import { useState } from 'react';
import {
    User,
    Building,
    Bell,
    Shield,
    Sliders,
    Save,
    Check,
} from 'lucide-react';

export default function Settings({ user }) {
    const [activeTab, setActiveTab] = useState('profile');
    const [saved, setSaved] = useState(false);

    const [profile, setProfile] = useState({
        name: user?.name || '',
        email: user?.email || '',
        role: user?.role || 'OPERATOR',
    });

    const [notifications, setNotifications] = useState({
        email: true,
        push: true,
        incidents: true,
        recommendations: true,
        reports: false,
    });

    const [thresholds, setThresholds] = useState({
        efficiency: 85,
        idleTime: 15,
        responseTime: 5,
        anomalySensitivity: 'medium',
    });

    const handleSave = () => {
        setSaved(true);
        setTimeout(() => setSaved(false), 2000);
    };

    const tabs = [
        { id: 'profile', label: 'Profile', icon: User },
        { id: 'organization', label: 'Organization', icon: Building },
        { id: 'notifications', label: 'Notifications', icon: Bell },
        { id: 'thresholds', label: 'Thresholds', icon: Sliders },
    ];

    return (
        <div className="space-y-6">
            {/* Header */}
            <div className="page-header">
                <h1 className="page-title">Settings</h1>
                <p className="page-subtitle">Manage your account and preferences</p>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
                {/* Tabs */}
                <div className="lg:col-span-1">
                    <div className="card p-2">
                        <nav className="space-y-1">
                            {tabs.map((tab) => (
                                <button
                                    key={tab.id}
                                    onClick={() => setActiveTab(tab.id)}
                                    className={`w-full flex items-center gap-3 px-4 py-2.5 rounded-lg text-left transition-colors ${activeTab === tab.id
                                            ? 'bg-primary-50 text-primary-700'
                                            : 'text-gray-600 hover:bg-gray-50'
                                        }`}
                                >
                                    <tab.icon className="w-5 h-5" />
                                    <span className="font-medium">{tab.label}</span>
                                </button>
                            ))}
                        </nav>
                    </div>
                </div>

                {/* Content */}
                <div className="lg:col-span-3">
                    <div className="card p-6">
                        {activeTab === 'profile' && (
                            <div className="space-y-6">
                                <h2 className="text-lg font-semibold text-gray-900">Profile Settings</h2>
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                    <div>
                                        <label className="block text-sm font-medium text-gray-700 mb-2">
                                            Full Name
                                        </label>
                                        <input
                                            type="text"
                                            value={profile.name}
                                            onChange={(e) => setProfile({ ...profile, name: e.target.value })}
                                            className="input"
                                        />
                                    </div>
                                    <div>
                                        <label className="block text-sm font-medium text-gray-700 mb-2">
                                            Email Address
                                        </label>
                                        <input
                                            type="email"
                                            value={profile.email}
                                            onChange={(e) => setProfile({ ...profile, email: e.target.value })}
                                            className="input"
                                        />
                                    </div>
                                    <div>
                                        <label className="block text-sm font-medium text-gray-700 mb-2">
                                            Role
                                        </label>
                                        <input
                                            type="text"
                                            value={profile.role}
                                            disabled
                                            className="input bg-gray-50 text-gray-500"
                                        />
                                    </div>
                                </div>
                            </div>
                        )}

                        {activeTab === 'organization' && (
                            <div className="space-y-6">
                                <h2 className="text-lg font-semibold text-gray-900">Organization Settings</h2>
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                    <div>
                                        <label className="block text-sm font-medium text-gray-700 mb-2">
                                            Organization Name
                                        </label>
                                        <input
                                            type="text"
                                            value={user?.organization?.name || ''}
                                            disabled
                                            className="input bg-gray-50 text-gray-500"
                                        />
                                    </div>
                                    <div>
                                        <label className="block text-sm font-medium text-gray-700 mb-2">
                                            Industry
                                        </label>
                                        <input
                                            type="text"
                                            value={user?.organization?.industry || ''}
                                            disabled
                                            className="input bg-gray-50 text-gray-500"
                                        />
                                    </div>
                                </div>
                            </div>
                        )}

                        {activeTab === 'notifications' && (
                            <div className="space-y-6">
                                <h2 className="text-lg font-semibold text-gray-900">Notification Preferences</h2>
                                <div className="space-y-4">
                                    {Object.entries(notifications).map(([key, value]) => (
                                        <label key={key} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg cursor-pointer hover:bg-gray-100 transition-colors">
                                            <div>
                                                <p className="font-medium text-gray-900 capitalize">{key.replace(/([A-Z])/g, ' $1').trim()}</p>
                                                <p className="text-sm text-gray-500">
                                                    {key === 'email' && 'Receive updates via email'}
                                                    {key === 'push' && 'Browser push notifications'}
                                                    {key === 'incidents' && 'Alerts for new incidents'}
                                                    {key === 'recommendations' && 'AI recommendation alerts'}
                                                    {key === 'reports' && 'Weekly summary reports'}
                                                </p>
                                            </div>
                                            <div className="relative">
                                                <input
                                                    type="checkbox"
                                                    checked={value}
                                                    onChange={(e) => setNotifications({ ...notifications, [key]: e.target.checked })}
                                                    className="sr-only"
                                                />
                                                <div className={`w-11 h-6 rounded-full transition-colors ${value ? 'bg-primary-600' : 'bg-gray-300'}`}>
                                                    <div className={`w-5 h-5 rounded-full bg-white shadow transform transition-transform ${value ? 'translate-x-5' : 'translate-x-0.5'} mt-0.5`} />
                                                </div>
                                            </div>
                                        </label>
                                    ))}
                                </div>
                            </div>
                        )}

                        {activeTab === 'thresholds' && (
                            <div className="space-y-6">
                                <h2 className="text-lg font-semibold text-gray-900">Detection Thresholds</h2>
                                <div className="space-y-6">
                                    <div>
                                        <div className="flex items-center justify-between mb-2">
                                            <label className="text-sm font-medium text-gray-700">
                                                Minimum Efficiency Target
                                            </label>
                                            <span className="text-sm font-semibold text-primary-600">{thresholds.efficiency}%</span>
                                        </div>
                                        <input
                                            type="range"
                                            min="50"
                                            max="100"
                                            value={thresholds.efficiency}
                                            onChange={(e) => setThresholds({ ...thresholds, efficiency: parseInt(e.target.value) })}
                                            className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-primary-600"
                                        />
                                    </div>
                                    <div>
                                        <div className="flex items-center justify-between mb-2">
                                            <label className="text-sm font-medium text-gray-700">
                                                Max Idle Time
                                            </label>
                                            <span className="text-sm font-semibold text-primary-600">{thresholds.idleTime} min</span>
                                        </div>
                                        <input
                                            type="range"
                                            min="5"
                                            max="60"
                                            value={thresholds.idleTime}
                                            onChange={(e) => setThresholds({ ...thresholds, idleTime: parseInt(e.target.value) })}
                                            className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-primary-600"
                                        />
                                    </div>
                                    <div>
                                        <label className="block text-sm font-medium text-gray-700 mb-2">
                                            Anomaly Detection Sensitivity
                                        </label>
                                        <select
                                            value={thresholds.anomalySensitivity}
                                            onChange={(e) => setThresholds({ ...thresholds, anomalySensitivity: e.target.value })}
                                            className="input"
                                        >
                                            <option value="low">Low - Fewer alerts, major anomalies only</option>
                                            <option value="medium">Medium - Balanced detection</option>
                                            <option value="high">High - More alerts, catch subtle changes</option>
                                        </select>
                                    </div>
                                </div>
                            </div>
                        )}

                        {/* Save Button */}
                        <div className="mt-8 pt-6 border-t border-gray-200 flex justify-end">
                            <button onClick={handleSave} className="btn-primary">
                                {saved ? (
                                    <>
                                        <Check className="w-4 h-4" />
                                        Saved
                                    </>
                                ) : (
                                    <>
                                        <Save className="w-4 h-4" />
                                        Save Changes
                                    </>
                                )}
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
