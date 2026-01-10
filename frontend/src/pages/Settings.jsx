import { useState } from 'react';
import { motion } from 'framer-motion';
import {
    User,
    Building2,
    Bell,
    Shield,
    Palette,
    Database,
    Save,
    Check,
} from 'lucide-react';

export default function Settings({ user }) {
    const [saved, setSaved] = useState(false);
    const [settings, setSettings] = useState({
        // Profile
        name: user?.name || 'John Admin',
        email: user?.email || 'admin@acme.com',

        // Organization
        orgName: user?.organization?.name || 'Acme Manufacturing Co.',
        industry: user?.organization?.industry || 'MANUFACTURING',
        costPerMinute: 75,

        // Notifications
        emailAlerts: true,
        criticalOnly: false,
        dailyDigest: true,
        weeklyReport: true,

        // Thresholds
        utilizationThreshold: 40,
        qualityThreshold: 85,
        idleTimeThreshold: 20,
    });

    const handleSave = () => {
        // In production, this would call the API
        setSaved(true);
        setTimeout(() => setSaved(false), 3000);
    };

    const industries = [
        { value: 'MANUFACTURING', label: 'Manufacturing' },
        { value: 'BPO', label: 'BPO / Call Center' },
        { value: 'LOGISTICS', label: 'Logistics & Warehousing' },
        { value: 'RETAIL', label: 'Retail' },
        { value: 'HEALTHCARE', label: 'Healthcare' },
        { value: 'GENERAL', label: 'General' },
    ];

    return (
        <div className="max-w-4xl mx-auto space-y-6">
            {/* Header */}
            <div>
                <h1 className="text-2xl lg:text-3xl font-display font-bold text-white">Settings</h1>
                <p className="text-dark-400 mt-1">Manage your account and preferences</p>
            </div>

            {/* Profile Section */}
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="glass-card"
            >
                <div className="flex items-center gap-3 mb-6">
                    <div className="p-2 rounded-lg bg-primary-500/20">
                        <User className="w-5 h-5 text-primary-400" />
                    </div>
                    <h2 className="text-lg font-semibold text-white">Profile</h2>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                        <label className="block text-sm font-medium text-dark-300 mb-2">Full Name</label>
                        <input
                            type="text"
                            value={settings.name}
                            onChange={(e) => setSettings({ ...settings, name: e.target.value })}
                            className="input"
                        />
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-dark-300 mb-2">Email</label>
                        <input
                            type="email"
                            value={settings.email}
                            onChange={(e) => setSettings({ ...settings, email: e.target.value })}
                            className="input"
                        />
                    </div>
                </div>
            </motion.div>

            {/* Organization Section */}
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.1 }}
                className="glass-card"
            >
                <div className="flex items-center gap-3 mb-6">
                    <div className="p-2 rounded-lg bg-accent-500/20">
                        <Building2 className="w-5 h-5 text-accent-400" />
                    </div>
                    <h2 className="text-lg font-semibold text-white">Organization</h2>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                        <label className="block text-sm font-medium text-dark-300 mb-2">Organization Name</label>
                        <input
                            type="text"
                            value={settings.orgName}
                            onChange={(e) => setSettings({ ...settings, orgName: e.target.value })}
                            className="input"
                        />
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-dark-300 mb-2">Industry</label>
                        <select
                            value={settings.industry}
                            onChange={(e) => setSettings({ ...settings, industry: e.target.value })}
                            className="input"
                        >
                            {industries.map((ind) => (
                                <option key={ind.value} value={ind.value}>{ind.label}</option>
                            ))}
                        </select>
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-dark-300 mb-2">
                            Cost per Minute (₹)
                        </label>
                        <input
                            type="number"
                            value={settings.costPerMinute}
                            onChange={(e) => setSettings({ ...settings, costPerMinute: Number(e.target.value) })}
                            className="input"
                        />
                        <p className="text-xs text-dark-500 mt-1">Used for loss calculations</p>
                    </div>
                </div>
            </motion.div>

            {/* Notifications Section */}
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2 }}
                className="glass-card"
            >
                <div className="flex items-center gap-3 mb-6">
                    <div className="p-2 rounded-lg bg-yellow-500/20">
                        <Bell className="w-5 h-5 text-yellow-400" />
                    </div>
                    <h2 className="text-lg font-semibold text-white">Notifications</h2>
                </div>

                <div className="space-y-4">
                    {[
                        { key: 'emailAlerts', label: 'Email Alerts', desc: 'Receive email notifications for anomalies' },
                        { key: 'criticalOnly', label: 'Critical Only', desc: 'Only notify for critical severity issues' },
                        { key: 'dailyDigest', label: 'Daily Digest', desc: 'Receive daily operational summary' },
                        { key: 'weeklyReport', label: 'Weekly Report', desc: 'Receive weekly performance report' },
                    ].map((item) => (
                        <div key={item.key} className="flex items-center justify-between p-4 rounded-xl bg-dark-800/50">
                            <div>
                                <p className="font-medium text-white">{item.label}</p>
                                <p className="text-sm text-dark-400">{item.desc}</p>
                            </div>
                            <label className="relative inline-flex items-center cursor-pointer">
                                <input
                                    type="checkbox"
                                    checked={settings[item.key]}
                                    onChange={(e) => setSettings({ ...settings, [item.key]: e.target.checked })}
                                    className="sr-only peer"
                                />
                                <div className="w-11 h-6 bg-dark-600 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary-600"></div>
                            </label>
                        </div>
                    ))}
                </div>
            </motion.div>

            {/* Detection Thresholds */}
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.3 }}
                className="glass-card"
            >
                <div className="flex items-center gap-3 mb-6">
                    <div className="p-2 rounded-lg bg-green-500/20">
                        <Database className="w-5 h-5 text-green-400" />
                    </div>
                    <h2 className="text-lg font-semibold text-white">Detection Thresholds</h2>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div>
                        <label className="block text-sm font-medium text-dark-300 mb-2">
                            Min Utilization (%)
                        </label>
                        <input
                            type="number"
                            min="0"
                            max="100"
                            value={settings.utilizationThreshold}
                            onChange={(e) => setSettings({ ...settings, utilizationThreshold: Number(e.target.value) })}
                            className="input"
                        />
                        <p className="text-xs text-dark-500 mt-1">Alert when below this</p>
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-dark-300 mb-2">
                            Min Quality Score (%)
                        </label>
                        <input
                            type="number"
                            min="0"
                            max="100"
                            value={settings.qualityThreshold}
                            onChange={(e) => setSettings({ ...settings, qualityThreshold: Number(e.target.value) })}
                            className="input"
                        />
                        <p className="text-xs text-dark-500 mt-1">Alert when below this</p>
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-dark-300 mb-2">
                            Max Idle Time (min)
                        </label>
                        <input
                            type="number"
                            min="0"
                            value={settings.idleTimeThreshold}
                            onChange={(e) => setSettings({ ...settings, idleTimeThreshold: Number(e.target.value) })}
                            className="input"
                        />
                        <p className="text-xs text-dark-500 mt-1">Alert when above this</p>
                    </div>
                </div>
            </motion.div>

            {/* Save Button */}
            <div className="flex justify-end">
                <button onClick={handleSave} className="btn-primary">
                    {saved ? (
                        <>
                            <Check className="w-5 h-5" />
                            Saved!
                        </>
                    ) : (
                        <>
                            <Save className="w-5 h-5" />
                            Save Changes
                        </>
                    )}
                </button>
            </div>
        </div>
    );
}
