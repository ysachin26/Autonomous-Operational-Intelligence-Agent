import { Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { PieChart } from 'lucide-react';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

const DataVisualization = ({ data }) => {
  if (!data) return null;

  const chartData = {
    labels: ['Budget', 'Authority', 'Need', 'Timeline'],
    datasets: [
      {
        label: 'BANT Score (0-10)',
        data: Object.values(data.bant),
        backgroundColor: 'rgba(75, 192, 192, 0.6)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 1,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: { position: 'top' },
      title: { display: true, text: 'BANT Analysis Breakdown' },
    },
    scales: {
      y: {
        beginAtZero: true,
        max: 10,
      },
    },
  };

  return (
    <div className="data-visualization card">
      <h3><PieChart size={20} /> Data Visualization</h3>
      <Bar data={chartData} options={chartOptions} />
    </div>
  );
};

export default DataVisualization;