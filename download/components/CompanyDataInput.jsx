import { useCallback } from 'react';
import { Building, Info, Mail, Phone, Globe } from 'lucide-react';

const CompanyDataInput = ({ data, onDataUpdate }) => {

  const handleChange = useCallback((e) => {
    const { name, value } = e.target;
    onDataUpdate({ [name]: value });
  }, [onDataUpdate]);

  const handleContactChange = useCallback((e) => {
    const { name, value } = e.target;
    onDataUpdate({ contact: { ...data.contact, [name]: value } });
  }, [data.contact, onDataUpdate]);

  return (
    <div className="company-data-input card">
      <h3><Building size={20} /> Company Information</h3>
      <div className="form-grid">
        <div className="input-group">
          <label>Company Name</label>
          <input
            type="text"
            name="name"
            value={data.name}
            onChange={handleChange}
            placeholder="e.g., Acme Corp"
          />
        </div>
        <div className="input-group">
          <label>Industry</label>
          <input
            type="text"
            name="industry"
            value={data.industry}
            onChange={handleChange}
            placeholder="e.g., SaaS, E-commerce"
          />
        </div>
        <div className="input-group full-width">
          <label>Description</label>
          <textarea
            name="description"
            value={data.description}
            onChange={handleChange}
            placeholder="Briefly describe the company..."
          />
        </div>
        <div className="input-group">
            <label><Mail size={16} /> Email</label>
            <input
              type="email"
              name="email"
              value={data.contact.email}
              onChange={handleContactChange}
              placeholder="contact@acme.com"
            />
        </div>
        <div className="input-group">
          <label><Phone size={16} /> Phone</label>
          <input
            type="tel"
            name="phone"
            value={data.contact.phone}
            onChange={handleContactChange}
            placeholder="+1-555-123-4567"
          />
        </div>
        <div className="input-group">
          <label><Globe size={16} /> Website</label>
          <input
            type="url"
            name="website"
            value={data.contact.website}
            onChange={handleContactChange}
            placeholder="https://acme.com"
          />
        </div>
      </div>
    </div>
  );
};

export default CompanyDataInput;