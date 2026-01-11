"""
AOIA ML Engine - Knowledge Graph Agent
Builds operational dependency maps for impact analysis.
"""

from typing import Dict, Any, Optional, List, Set
from datetime import datetime
import uuid

from app.agents.base_agent import BaseAgent


class KnowledgeGraphAgent(BaseAgent):
    """
    Knowledge Graph Agent - Builds operational dependency maps.
    
    Maps relationships between:
    - Machines → Operators → Tasks → Workflows
    - Tracks dependency chains for cascading impact analysis
    
    Inputs: Events and relationships from operational data
    Outputs: Dependency chains, affected nodes on anomalies
    """
    
    def __init__(self):
        super().__init__("knowledge_graph")
        
        # Graph structure: node_id -> {type, connections, metadata}
        self.nodes: Dict[str, Dict[str, Any]] = {}
        
        # Edges: (from_id, to_id) -> {type, weight, metadata}
        self.edges: Dict[tuple, Dict[str, Any]] = {}
        
        # Reverse index for quick lookups
        self.type_index: Dict[str, Set[str]] = {
            "machine": set(),
            "operator": set(),
            "task": set(),
            "workflow": set(),
            "process": set(),
        }
    
    def process(
        self, 
        input_data: Dict[str, Any], 
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Build/update knowledge graph from operational data.
        
        Args:
            input_data: Contains machines, workflows, shifts, events, detections
            context: Optional - detections to analyze for impact
            
        Returns:
            Graph stats and affected nodes if detections provided
        """
        start_time = self._start_processing()
        
        try:
            # Build graph from input data
            self._build_graph_from_data(input_data)
            
            # If detections provided in context, find affected nodes
            affected_analysis = None
            if context and context.get("detections"):
                affected_analysis = self._analyze_impact(context["detections"])
            
            self._complete_processing(start_time, success=True)
            
            result = {
                "status": "success",
                "graph_stats": {
                    "total_nodes": len(self.nodes),
                    "total_edges": len(self.edges),
                    "machines": len(self.type_index.get("machine", set())),
                    "operators": len(self.type_index.get("operator", set())),
                    "tasks": len(self.type_index.get("task", set())),
                },
                "processing_time_ms": (datetime.now() - start_time).total_seconds() * 1000,
            }
            
            if affected_analysis:
                result["affected_nodes"] = affected_analysis
            
            return result
            
        except Exception as e:
            self._log_error(e, "Knowledge graph processing failed")
            self._complete_processing(start_time, success=False)
            return {"status": "error", "error": str(e)}
    
    def _build_graph_from_data(self, input_data: Dict[str, Any]) -> None:
        """Build knowledge graph from operational data."""
        machines = input_data.get("machines", [])
        workflows = input_data.get("workflows", [])
        shifts = input_data.get("shifts", [])
        
        # Add machine nodes
        for machine in machines:
            machine_id = machine.get("machine_id")
            if machine_id:
                self._add_node(machine_id, "machine", {
                    "state": machine.get("machine_state"),
                    "output": machine.get("output_per_min"),
                })
        
        # Add operator nodes and link to machines/tasks
        for shift in shifts:
            operator_id = shift.get("operator_id")
            if operator_id:
                self._add_node(operator_id, "operator", {
                    "load": shift.get("operator_load"),
                    "shift_output": shift.get("shift_output"),
                })
                
                # Link operator to assigned tasks
                for task_id in shift.get("task_assignments", []):
                    self._add_edge(operator_id, task_id, "operates", weight=1.0)
        
        # Add task nodes and link to workflows
        for workflow in workflows:
            task_id = workflow.get("task_id")
            if task_id:
                self._add_node(task_id, "task", {
                    "duration": workflow.get("task_duration"),
                    "rework_loops": workflow.get("rework_loops"),
                    "status": workflow.get("status"),
                })
                
                # Link tasks in sequence
                sequence = workflow.get("process_sequence", [])
                for i in range(len(sequence) - 1):
                    self._add_edge(sequence[i], sequence[i+1], "precedes", weight=1.0)
        
        # Infer machine-task relationships
        self._infer_machine_task_relationships(machines, workflows)
    
    def _add_node(self, node_id: str, node_type: str, metadata: Dict[str, Any]) -> None:
        """Add or update a node in the graph."""
        self.nodes[node_id] = {
            "id": node_id,
            "type": node_type,
            "metadata": metadata,
            "updated_at": datetime.now().isoformat(),
        }
        self.type_index[node_type].add(node_id)
    
    def _add_edge(
        self, 
        from_id: str, 
        to_id: str, 
        edge_type: str, 
        weight: float = 1.0,
        metadata: Optional[Dict] = None
    ) -> None:
        """Add an edge between two nodes."""
        self.edges[(from_id, to_id)] = {
            "type": edge_type,
            "weight": weight,
            "metadata": metadata or {},
            "created_at": datetime.now().isoformat(),
        }
    
    def _infer_machine_task_relationships(
        self, 
        machines: List[Dict], 
        workflows: List[Dict]
    ) -> None:
        """Infer relationships between machines and tasks."""
        # Simple heuristic: distribute tasks across machines
        machine_ids = [m.get("machine_id") for m in machines if m.get("machine_id")]
        task_ids = [w.get("task_id") for w in workflows if w.get("task_id")]
        
        if machine_ids and task_ids:
            for i, task_id in enumerate(task_ids):
                machine_id = machine_ids[i % len(machine_ids)]
                self._add_edge(machine_id, task_id, "processes", weight=0.8)
    
    def _analyze_impact(self, detections: List[Dict]) -> Dict[str, Any]:
        """Analyze cascading impact of detected anomalies."""
        affected_machines: Set[str] = set()
        affected_operators: Set[str] = set()
        affected_tasks: Set[str] = set()
        dependency_chains: List[Dict] = []
        
        for detection in detections:
            location = detection.get("anomaly_location")
            location_type = detection.get("location_type", "")
            
            if not location:
                continue
            
            # Find all connected nodes
            connected = self._get_connected_nodes(location, max_depth=3)
            
            for node_id, depth in connected.items():
                node = self.nodes.get(node_id, {})
                node_type = node.get("type", "")
                
                if node_type == "machine":
                    affected_machines.add(node_id)
                elif node_type == "operator":
                    affected_operators.add(node_id)
                elif node_type in ["task", "process"]:
                    affected_tasks.add(node_id)
            
            # Build dependency chain
            chain = self._build_dependency_chain(location)
            if chain:
                dependency_chains.append({
                    "source": location,
                    "source_type": location_type,
                    "chain": chain,
                    "impact_score": len(connected) / max(len(self.nodes), 1),
                })
        
        return {
            "affected_machines": list(affected_machines),
            "affected_operators": list(affected_operators),
            "affected_tasks": list(affected_tasks),
            "dependency_chains": dependency_chains,
            "total_affected": len(affected_machines) + len(affected_operators) + len(affected_tasks),
        }
    
    def _get_connected_nodes(
        self, 
        start_node: str, 
        max_depth: int = 3
    ) -> Dict[str, int]:
        """Get all nodes connected to start_node within max_depth."""
        visited: Dict[str, int] = {}
        queue = [(start_node, 0)]
        
        while queue:
            node_id, depth = queue.pop(0)
            
            if node_id in visited or depth > max_depth:
                continue
            
            visited[node_id] = depth
            
            # Find connected nodes via edges
            for (from_id, to_id), edge in self.edges.items():
                if from_id == node_id and to_id not in visited:
                    queue.append((to_id, depth + 1))
                elif to_id == node_id and from_id not in visited:
                    queue.append((from_id, depth + 1))
        
        return visited
    
    def _build_dependency_chain(self, start_node: str) -> List[Dict[str, Any]]:
        """Build a human-readable dependency chain from a node."""
        chain = []
        visited = set()
        current = start_node
        
        while current and current not in visited:
            visited.add(current)
            node = self.nodes.get(current, {})
            
            chain.append({
                "node_id": current,
                "node_type": node.get("type", "unknown"),
                "metadata": node.get("metadata", {}),
            })
            
            # Find next in chain
            next_node = None
            for (from_id, to_id), edge in self.edges.items():
                if from_id == current and to_id not in visited:
                    next_node = to_id
                    break
            
            current = next_node
            
            if len(chain) >= 5:  # Limit chain length
                break
        
        return chain
    
    def get_graph_snapshot(self) -> Dict[str, Any]:
        """Get a snapshot of the current knowledge graph."""
        return {
            "nodes": self.nodes,
            "edges": {f"{k[0]}->{k[1]}": v for k, v in self.edges.items()},
            "type_counts": {k: len(v) for k, v in self.type_index.items()},
            "timestamp": datetime.now().isoformat(),
        }
    
    def clear_graph(self) -> None:
        """Clear the knowledge graph."""
        self.nodes.clear()
        self.edges.clear()
        for key in self.type_index:
            self.type_index[key].clear()
