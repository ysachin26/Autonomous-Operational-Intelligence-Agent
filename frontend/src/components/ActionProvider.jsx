import { useState, createContext, useContext } from 'react';
import { CheckCircle, X, AlertTriangle, Loader2, Clock } from 'lucide-react';

// Action context for global action management
const ActionContext = createContext(null);

export function ActionProvider({ children }) {
    const [pendingAction, setPendingAction] = useState(null);
    const [executedActions, setExecutedActions] = useState([]);
    const [showNotification, setShowNotification] = useState(null);

    const requestAction = (action) => {
        setPendingAction(action);
    };

    const confirmAction = async () => {
        if (!pendingAction) return;

        const action = { ...pendingAction, status: 'executing', startedAt: new Date() };
        setPendingAction({ ...action, status: 'executing' });

        // Simulate action execution (2-4 seconds)
        await new Promise(resolve => setTimeout(resolve, 2000 + Math.random() * 2000));

        const completedAction = {
            ...action,
            id: `ACT-${Date.now()}`,
            status: 'completed',
            completedAt: new Date(),
        };

        setExecutedActions(prev => [completedAction, ...prev]);
        setPendingAction(null);

        // Show success notification
        setShowNotification({
            type: 'success',
            title: 'Action Executed',
            message: `${action.title} has been completed successfully.`,
            impact: action.impact,
        });

        // Auto-hide notification after 5 seconds
        setTimeout(() => setShowNotification(null), 5000);
    };

    const cancelAction = () => {
        setPendingAction(null);
    };

    const dismissNotification = () => {
        setShowNotification(null);
    };

    return (
        <ActionContext.Provider value={{
            requestAction,
            executedActions,
            pendingAction,
        }}>
            {children}

            {/* Confirmation Modal */}
            {pendingAction && (
                <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50">
                    <div className="bg-white rounded-xl shadow-2xl max-w-md w-full p-6">
                        {pendingAction.status === 'executing' ? (
                            // Executing state
                            <div className="text-center py-8">
                                <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-primary-100 flex items-center justify-center">
                                    <Loader2 className="w-8 h-8 text-primary-600 animate-spin" />
                                </div>
                                <h3 className="text-lg font-semibold text-gray-900 mb-2">
                                    Executing Action...
                                </h3>
                                <p className="text-gray-500">{pendingAction.title}</p>
                                <div className="mt-4 flex items-center justify-center gap-2 text-sm text-gray-400">
                                    <Clock className="w-4 h-4" />
                                    This may take a few seconds
                                </div>
                            </div>
                        ) : (
                            // Confirmation state
                            <>
                                <div className="flex items-start gap-4 mb-6">
                                    <div className="w-12 h-12 rounded-xl bg-amber-100 flex items-center justify-center flex-shrink-0">
                                        <AlertTriangle className="w-6 h-6 text-amber-600" />
                                    </div>
                                    <div>
                                        <h3 className="text-lg font-semibold text-gray-900">
                                            Confirm Action
                                        </h3>
                                        <p className="text-sm text-gray-500 mt-1">
                                            You are about to execute an autonomous action
                                        </p>
                                    </div>
                                </div>

                                <div className="bg-gray-50 rounded-lg p-4 mb-6">
                                    <h4 className="font-semibold text-gray-900 mb-2">
                                        {pendingAction.title}
                                    </h4>
                                    {pendingAction.description && (
                                        <p className="text-sm text-gray-600 mb-3">
                                            {pendingAction.description}
                                        </p>
                                    )}
                                    <div className="flex items-center gap-4 text-sm">
                                        <span className="text-accent-600 font-medium">
                                            +₹{pendingAction.impact?.toLocaleString()} potential savings
                                        </span>
                                        {pendingAction.confidence && (
                                            <span className="text-gray-500">
                                                {pendingAction.confidence}% confidence
                                            </span>
                                        )}
                                    </div>
                                </div>

                                <div className="bg-blue-50 border border-blue-200 rounded-lg p-3 mb-6">
                                    <p className="text-sm text-blue-800">
                                        <strong>What will happen:</strong> {pendingAction.action || 'The system will automatically implement this recommendation and update relevant schedules/settings.'}
                                    </p>
                                </div>

                                <div className="flex gap-3">
                                    <button
                                        onClick={cancelAction}
                                        className="flex-1 btn-secondary"
                                    >
                                        Cancel
                                    </button>
                                    <button
                                        onClick={confirmAction}
                                        className="flex-1 btn-primary"
                                    >
                                        Confirm & Execute
                                    </button>
                                </div>
                            </>
                        )}
                    </div>
                </div>
            )}

            {/* Success Notification */}
            {showNotification && (
                <div className="fixed bottom-4 right-4 z-50 max-w-sm animate-slide-up">
                    <div className={`rounded-xl shadow-lg p-4 ${showNotification.type === 'success'
                            ? 'bg-accent-600 text-white'
                            : 'bg-white border border-gray-200'
                        }`}>
                        <div className="flex items-start gap-3">
                            <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${showNotification.type === 'success'
                                    ? 'bg-white/20'
                                    : 'bg-accent-100'
                                }`}>
                                <CheckCircle className={`w-5 h-5 ${showNotification.type === 'success'
                                        ? 'text-white'
                                        : 'text-accent-600'
                                    }`} />
                            </div>
                            <div className="flex-1">
                                <h4 className="font-semibold">
                                    {showNotification.title}
                                </h4>
                                <p className={`text-sm mt-1 ${showNotification.type === 'success'
                                        ? 'text-white/80'
                                        : 'text-gray-500'
                                    }`}>
                                    {showNotification.message}
                                </p>
                                {showNotification.impact && (
                                    <p className={`text-sm font-medium mt-2 ${showNotification.type === 'success'
                                            ? 'text-white'
                                            : 'text-accent-600'
                                        }`}>
                                        +₹{showNotification.impact.toLocaleString()} saved
                                    </p>
                                )}
                            </div>
                            <button
                                onClick={dismissNotification}
                                className={`p-1 rounded-lg ${showNotification.type === 'success'
                                        ? 'hover:bg-white/20'
                                        : 'hover:bg-gray-100'
                                    }`}
                            >
                                <X className="w-4 h-4" />
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </ActionContext.Provider>
    );
}

export function useActions() {
    const context = useContext(ActionContext);
    if (!context) {
        throw new Error('useActions must be used within ActionProvider');
    }
    return context;
}
