import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import './App.css';
import { fetchProperties, fetchTenants, createPropertyWithTenant, createTenant, updateProperty, deleteProperty, updateTenant, deleteTenant } from './services/api';

// Simple page components
// Update Dashboard to accept properties, setProperties, locations, setLocations as props
const Dashboard = ({ properties, setProperties, locations, setLocations, createPropertyWithTenant }: {
  properties: any[],
  setProperties: React.Dispatch<React.SetStateAction<any[]>>,
  locations: string[],
  setLocations: React.Dispatch<React.SetStateAction<string[]>>,
  createPropertyWithTenant: (payload: any) => Promise<any>
}) => {
  const [selectedLocation, setSelectedLocation] = useState('All Locations');
  const [showAddProperty, setShowAddProperty] = useState(false);

  // Add state for property fields
  const [propertyName, setPropertyName] = useState('');
  const [propertyLocation, setPropertyLocation] = useState('');
  const [propertyType, setPropertyType] = useState('');
  const [monthlyRent, setMonthlyRent] = useState('');
  // Add Location inline in Add Property
  const [isAddingNewLocation, setIsAddingNewLocation] = useState(false);
  const [newLocationName, setNewLocationName] = useState('');

  // Add state for tenant fields
  const [tenantFirstName, setTenantFirstName] = useState('');
  const [tenantLastName, setTenantLastName] = useState('');
  const [tenantEmail, setTenantEmail] = useState('');
  const [tenantPhone, setTenantPhone] = useState('');

  // --- PROPERTIES CRUD ---
  // Add state for editing property
  const [editingProperty, setEditingProperty] = useState<any | null>(null);
  const [propertyEditLoading, setPropertyEditLoading] = useState(false);
  const [propertyEditError, setPropertyEditError] = useState<string | null>(null);

  const handleEditProperty = (property: any) => {
    setEditingProperty(property);
    setPropertyEditError(null);
  };

  const handleUpdateProperty = async (e: React.FormEvent) => {
    e.preventDefault();
    setPropertyEditLoading(true);
    setPropertyEditError(null);
    try {
      const allowedUpdate: any = {
        title: editingProperty.title,
        description: editingProperty.description,
        address: editingProperty.address,
        city: editingProperty.city,
        state: editingProperty.state,
        zip_code: editingProperty.zip_code,
        country: editingProperty.country,
        property_type: editingProperty.property_type,
        bedrooms: editingProperty.bedrooms,
        bathrooms: editingProperty.bathrooms,
        square_feet: editingProperty.square_feet,
        year_built: editingProperty.year_built,
        monthly_rent: editingProperty.monthly_rent,
        security_deposit: editingProperty.security_deposit,
        utilities_included: editingProperty.utilities_included,
        is_available: editingProperty.is_available,
        is_active: editingProperty.is_active,
      };
      const response = await updateProperty(editingProperty.id, allowedUpdate);
      const updated = response.data;
      setProperties(prev => prev.map(p => p.id === updated.id ? updated : p));
      setEditingProperty(null);
    } catch (err) {
      setPropertyEditError('Failed to update property');
    } finally {
      setPropertyEditLoading(false);
    }
  };

  const handleDeleteProperty = async (id: number) => {
    if (!window.confirm('Are you sure you want to delete this property?')) return;
    try {
      await deleteProperty(id);
      setProperties(prev => prev.filter(p => p.id !== id));
    } catch {
      alert('Failed to delete property');
    }
  };

  const filteredProperties = selectedLocation === 'All Locations'
    ? properties
    : properties.filter(property => property.city === selectedLocation);

  // Handle property form submission
  const handleAddProperty = async (e: React.FormEvent) => {
    e.preventDefault();
    // Determine final location (either selected or newly added)
    const trimmedNewLocation = newLocationName.trim();
    const finalLocation = isAddingNewLocation && trimmedNewLocation
      ? trimmedNewLocation
      : propertyLocation;

    // Construct payload
    const payload: any = {
      title: propertyName,
      address: propertyName, // For demo, using name as address
      city: finalLocation,
      state: '',
      zip_code: '',
      country: 'USA',
      property_type: propertyType,
      monthly_rent: parseFloat(monthlyRent.replace(/[^0-9.]/g, '')) || 0,
      // Add other property fields as needed
    };
    // If tenant details are filled, add tenant object
    if (tenantFirstName && tenantLastName && tenantEmail && tenantPhone) {
      payload.tenant = {
        first_name: tenantFirstName,
        last_name: tenantLastName,
        email: tenantEmail,
        phone: tenantPhone,
      };
    }
    // Send to backend (replace with actual API call)
    try {
      const response = await createPropertyWithTenant(payload);
      const newProperty = response.data;
      setProperties(prev => [...prev, newProperty]);
      // If a new location was added, persist it to the locations list
      if (isAddingNewLocation && finalLocation && !locations.includes(finalLocation)) {
        setLocations(prev => [...prev, finalLocation]);
      }
      alert('Property and tenant details submitted!');
      setShowAddProperty(false);
      // Reset form fields
      setPropertyName('');
      setPropertyLocation('');
      setPropertyType('');
      setMonthlyRent('');
      setTenantFirstName('');
      setTenantLastName('');
      setTenantEmail('');
      setTenantPhone('');
      setIsAddingNewLocation(false);
      setNewLocationName('');
    } catch (err) {
      alert('Error submitting property');
    }
  };

  return (
    <div className="page">
      <div className="dashboard-header">
        <h2>Dashboard</h2>
        <div className="dashboard-actions">
          <button 
            className="btn btn-primary" 
            onClick={() => setShowAddProperty(true)}
          >
            + Add Property
          </button>
        </div>
      </div>

      <div className="stats-grid">
        <div className="stat-card">
          <h3>Total Properties</h3>
          <p className="stat-number">12</p>
        </div>
        <div className="stat-card">
          <h3>Active Tenants</h3>
          <p className="stat-number">8</p>
        </div>
        <div className="stat-card">
          <h3>Monthly Revenue</h3>
          <p className="stat-number">$24,500</p>
        </div>
        <div className="stat-card">
          <h3>Pending Issues</h3>
          <p className="stat-number">3</p>
        </div>
      </div>

      <div className="properties-section">
        <div className="section-header">
          <h3>Properties Overview</h3>
          <div className="filter-controls">
            <label htmlFor="location-filter">Filter by Location:</label>
            <select 
              id="location-filter"
              value={selectedLocation} 
              onChange={(e) => setSelectedLocation(e.target.value)}
              className="location-dropdown"
            >
              {locations.map(location => (
                <option key={location} value={location}>
                  {location}
                </option>
              ))}
            </select>
          </div>
        </div>

        <div className="property-list">
            {filteredProperties.length === 0 ? (
            <div className="empty-state">No properties found.</div>
          ) : (
            filteredProperties.map(property => (
              <div key={property.id} className="property-card">
                <h3>{property.title}</h3>
                <p className="property-location">{property.city}</p>
                <p>{property.property_type} - ${property.monthly_rent}</p>
                <span className={`status ${property.is_active ? 'active' : 'inactive'}`}>{property.is_active ? 'Active' : 'Inactive'}</span>
                <button onClick={() => handleEditProperty(property)}>Edit</button>
                <button onClick={() => handleDeleteProperty(property.id)}>Delete</button>
              </div>
            ))
          )}
        </div>
      </div>

      {/* Add Property Modal */}
      {showAddProperty && (
        <div className="modal-overlay">
          <div className="modal">
            <div className="modal-header">
              <h3>Add New Property</h3>
              <button 
                className="modal-close" 
                onClick={() => setShowAddProperty(false)}
              >
                ×
              </button>
            </div>
            <div className="modal-body">
              <form className="property-form" onSubmit={handleAddProperty}>
                <div className="form-group">
                  <label>Property Name:</label>
                  <input type="text" placeholder="e.g., 123 Main Street" value={propertyName} onChange={e => setPropertyName(e.target.value)} />
                </div>
                <div className="form-group">
                  <label>Location:</label>
                  {isAddingNewLocation ? (
                    <>
                      <input
                        type="text"
                        placeholder="Enter new location"
                        value={newLocationName}
                        onChange={e => setNewLocationName(e.target.value)}
                      />
                      <button
                        type="button"
                        className="btn btn-secondary"
                        onClick={() => { setIsAddingNewLocation(false); setNewLocationName(''); }}
                      >
                        Use existing location
                      </button>
                    </>
                  ) : (
                    <>
                      <select
                        value={propertyLocation}
                        onChange={e => setPropertyLocation(e.target.value)}
                      >
                        <option value="">Select location</option>
                        {locations.map(location => (
                          <option key={location} value={location}>{location}</option>
                        ))}
                      </select>
                      <button
                        type="button"
                        className="btn btn-secondary"
                        onClick={() => setIsAddingNewLocation(true)}
                      >
                        + Add new location
                      </button>
                    </>
                  )}
                </div>
                <div className="form-group">
                  <label>Property Type:</label>
                  <input type="text" placeholder="e.g., 3 Bed, 2 Bath" value={propertyType} onChange={e => setPropertyType(e.target.value)} />
                </div>
                <div className="form-group">
                  <label>Monthly Rent:</label>
                  <input type="text" placeholder="e.g., $2,200" value={monthlyRent} onChange={e => setMonthlyRent(e.target.value)} />
                </div>
                <hr />
                <h4>Tenant Details (optional)</h4>
                <div className="form-group">
                  <label>First Name:</label>
                  <input type="text" placeholder="Tenant first name" value={tenantFirstName} onChange={e => setTenantFirstName(e.target.value)} />
                </div>
                <div className="form-group">
                  <label>Last Name:</label>
                  <input type="text" placeholder="Tenant last name" value={tenantLastName} onChange={e => setTenantLastName(e.target.value)} />
                </div>
                <div className="form-group">
                  <label>Email:</label>
                  <input type="email" placeholder="Tenant email" value={tenantEmail} onChange={e => setTenantEmail(e.target.value)} />
                </div>
                <div className="form-group">
                  <label>Phone:</label>
                  <input type="text" placeholder="Tenant phone" value={tenantPhone} onChange={e => setTenantPhone(e.target.value)} />
                </div>
                <div className="form-actions">
                  <button type="button" className="btn btn-secondary" onClick={() => setShowAddProperty(false)}>
                    Cancel
                  </button>
                  <button type="submit" className="btn btn-primary">
                    Add Property
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}

      {/* Edit Property Modal */}
      {editingProperty && (
        <div className="modal-overlay">
          <div className="modal">
            <div className="modal-header">
              <h3>Edit Property</h3>
              <button className="modal-close" onClick={() => setEditingProperty(null)}>×</button>
            </div>
            <div className="modal-body">
              <form className="property-form" onSubmit={handleUpdateProperty}>
                <div className="form-group">
                  <label>Title:</label>
                  <input type="text" value={editingProperty.title} onChange={e => setEditingProperty({ ...editingProperty, title: e.target.value })} />
                </div>
                <div className="form-group">
                  <label>City:</label>
                  <select value={editingProperty.city} onChange={e => setEditingProperty({ ...editingProperty, city: e.target.value })}>
                    {locations.map(location => (
                      <option key={location} value={location}>{location}</option>
                    ))}
                  </select>
                </div>
                <div className="form-group">
                  <label>Property Type:</label>
                  <input type="text" value={editingProperty.property_type || ''} onChange={e => setEditingProperty({ ...editingProperty, property_type: e.target.value })} />
                </div>
                <div className="form-group">
                  <label>Monthly Rent:</label>
                  <input type="number" value={editingProperty.monthly_rent ?? ''} onChange={e => setEditingProperty({ ...editingProperty, monthly_rent: Number(e.target.value) })} />
                </div>
                <div className="form-group">
                  <label>Status:</label>
                  <select value={editingProperty.is_active ? 'true' : 'false'} onChange={e => setEditingProperty({ ...editingProperty, is_active: e.target.value === 'true' })}>
                    <option value="true">Active</option>
                    <option value="false">Inactive</option>
                  </select>
                </div>
                <div className="form-actions">
                  <button type="button" className="btn btn-secondary" onClick={() => setEditingProperty(null)}>
                    Cancel
                  </button>
                  <button type="submit" className="btn btn-primary" disabled={propertyEditLoading}>
                    {propertyEditLoading ? 'Updating...' : 'Update Property'}
                  </button>
                </div>
                {propertyEditError && <div style={{ color: 'red' }}>{propertyEditError}</div>}
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

const Properties = ({ properties, setProperties, locations, setLocations, createPropertyWithTenant }: {
  properties: any[],
  setProperties: React.Dispatch<React.SetStateAction<any[]>>,
  locations: string[],
  setLocations: React.Dispatch<React.SetStateAction<string[]>>,
  createPropertyWithTenant: (payload: any) => Promise<any>
}) => {
  const [selectedLocation, setSelectedLocation] = useState('All Locations');
  const [showAddProperty, setShowAddProperty] = useState(false);

  // Add state for property fields
  const [propertyName, setPropertyName] = useState('');
  const [propertyLocation, setPropertyLocation] = useState('');
  const [propertyType, setPropertyType] = useState('');
  const [monthlyRent, setMonthlyRent] = useState('');
  const [isAddingNewLocation, setIsAddingNewLocation] = useState(false);
  const [newLocationName, setNewLocationName] = useState('');

  // Add state for tenant fields
  const [tenantFirstName, setTenantFirstName] = useState('');
  const [tenantLastName, setTenantLastName] = useState('');
  const [tenantEmail, setTenantEmail] = useState('');
  const [tenantPhone, setTenantPhone] = useState('');

  const filteredProperties = selectedLocation === 'All Locations'
    ? properties
    : properties.filter(property => property.city === selectedLocation);

  const handleAddProperty = async (e: React.FormEvent) => {
    e.preventDefault();
    const trimmedNewLocation = newLocationName.trim();
    const finalLocation = isAddingNewLocation && trimmedNewLocation
      ? trimmedNewLocation
      : propertyLocation;

    const payload: any = {
      title: propertyName,
      address: propertyName,
      city: finalLocation,
      state: '',
      zip_code: '',
      country: 'USA',
      property_type: propertyType,
      monthly_rent: parseFloat(monthlyRent.replace(/[^0-9.]/g, '')) || 0,
    };

    if (tenantFirstName && tenantLastName && tenantEmail && tenantPhone) {
      payload.tenant = {
        first_name: tenantFirstName,
        last_name: tenantLastName,
        email: tenantEmail,
        phone: tenantPhone,
      };
    }

    try {
      const response = await createPropertyWithTenant(payload);
      const newProperty = response.data;
      setProperties(prev => [...prev, newProperty]);
      if (isAddingNewLocation && finalLocation && !locations.includes(finalLocation)) {
        setLocations(prev => [...prev, finalLocation]);
      }
      alert('Property and tenant details submitted!');
      setShowAddProperty(false);
      setPropertyName('');
      setPropertyLocation('');
      setPropertyType('');
      setMonthlyRent('');
      setTenantFirstName('');
      setTenantLastName('');
      setTenantEmail('');
      setTenantPhone('');
      setIsAddingNewLocation(false);
      setNewLocationName('');
    } catch (err) {
      alert('Error submitting property');
    }
  };

  return (
    <div className="page">
      <div className="properties-header">
        <h2>Properties</h2>
        <div className="properties-actions">
          <button 
            className="btn btn-primary" 
            onClick={() => setShowAddProperty(true)}
          >
            + Add Property
          </button>
        </div>
      </div>

      <div className="properties-section">
        <div className="section-header">
          <h3>Properties Overview</h3>
          <div className="filter-controls">
            <label htmlFor="location-filter">Filter by Location:</label>
            <select 
              id="location-filter"
              value={selectedLocation} 
              onChange={(e) => setSelectedLocation(e.target.value)}
              className="location-dropdown"
            >
              <option value="All Locations">All Locations</option>
              {locations.map(location => (
                <option key={location} value={location}>
                  {location}
                </option>
              ))}
            </select>
          </div>
        </div>

        <div className="property-list">
          {filteredProperties.length === 0 ? (
            <div className="empty-state">No properties found.</div>
          ) : (
            filteredProperties.map(property => (
              <div key={property.id} className="property-card">
                <h3>{property.title}</h3>
                <p className="property-location">{property.city}</p>
                <p>{property.property_type} - ${property.monthly_rent}</p>
                <span className={`status ${property.is_active ? 'active' : 'inactive'}`}>
                  {property.is_active ? 'Active' : 'Inactive'}
                </span>
              </div>
            ))
          )}
        </div>
      </div>

      {/* Add Property Modal */}
      {showAddProperty && (
        <div className="modal-overlay">
          <div className="modal">
            <div className="modal-header">
              <h3>Add New Property</h3>
              <button 
                className="modal-close" 
                onClick={() => setShowAddProperty(false)}
              >
                ×
              </button>
            </div>
            <div className="modal-body">
              <form className="property-form" onSubmit={handleAddProperty}>
                <div className="form-group">
                  <label>Property Name:</label>
                  <input type="text" placeholder="e.g., 123 Main Street" value={propertyName} onChange={e => setPropertyName(e.target.value)} />
                </div>
                <div className="form-group">
                  <label>Location:</label>
                  {isAddingNewLocation ? (
                    <>
                      <input
                        type="text"
                        placeholder="Enter new location"
                        value={newLocationName}
                        onChange={e => setNewLocationName(e.target.value)}
                      />
                      <button
                        type="button"
                        className="btn btn-secondary"
                        onClick={() => { setIsAddingNewLocation(false); setNewLocationName(''); }}
                      >
                        Use existing location
                      </button>
                    </>
                  ) : (
                    <>
                      <select
                        value={propertyLocation}
                        onChange={e => setPropertyLocation(e.target.value)}
                      >
                        <option value="">Select location</option>
                        {locations.map(location => (
                          <option key={location} value={location}>{location}</option>
                        ))}
                      </select>
                      <button
                        type="button"
                        className="btn btn-secondary"
                        onClick={() => setIsAddingNewLocation(true)}
                      >
                        + Add new location
                      </button>
                    </>
                  )}
                </div>
                <div className="form-group">
                  <label>Property Type:</label>
                  <input type="text" placeholder="e.g., 3 Bed, 2 Bath" value={propertyType} onChange={e => setPropertyType(e.target.value)} />
                </div>
                <div className="form-group">
                  <label>Monthly Rent:</label>
                  <input type="text" placeholder="e.g., $2,200" value={monthlyRent} onChange={e => setMonthlyRent(e.target.value)} />
                </div>
                <hr />
                <h4>Tenant Details (optional)</h4>
                <div className="form-group">
                  <label>First Name:</label>
                  <input type="text" placeholder="Tenant first name" value={tenantFirstName} onChange={e => setTenantFirstName(e.target.value)} />
                </div>
                <div className="form-group">
                  <label>Last Name:</label>
                  <input type="text" placeholder="Tenant last name" value={tenantLastName} onChange={e => setTenantLastName(e.target.value)} />
                </div>
                <div className="form-group">
                  <label>Email:</label>
                  <input type="email" placeholder="Tenant email" value={tenantEmail} onChange={e => setTenantEmail(e.target.value)} />
                </div>
                <div className="form-group">
                  <label>Phone:</label>
                  <input type="text" placeholder="Tenant phone" value={tenantPhone} onChange={e => setTenantPhone(e.target.value)} />
                </div>
                <div className="form-actions">
                  <button type="button" className="btn btn-secondary" onClick={() => setShowAddProperty(false)}>
                    Cancel
                  </button>
                  <button type="submit" className="btn btn-primary">
                    Add Property
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

// Update Tenants to accept properties as a prop
const Tenants = ({ properties, tenants, setTenants, createTenant }: {
  properties: any[],
  tenants: any[],
  setTenants: React.Dispatch<React.SetStateAction<any[]>>,
  createTenant: (payload: any) => Promise<any>
}) => {
  const [showAddTenant, setShowAddTenant] = useState(false);
  const [tenantFirstName, setTenantFirstName] = useState('');
  const [tenantLastName, setTenantLastName] = useState('');
  const [tenantEmail, setTenantEmail] = useState('');
  const [tenantPhone, setTenantPhone] = useState('');
  const [tenantProperty, setTenantProperty] = useState('');
  // const [tenants, setTenants] = useState<any[]>([]); // This state is now passed as a prop

  // --- TENANTS CRUD ---
  const [editingTenant, setEditingTenant] = useState<any | null>(null);
  const [tenantEditLoading, setTenantEditLoading] = useState(false);
  const [tenantEditError, setTenantEditError] = useState<string | null>(null);

  const handleEditTenant = (tenant: any) => {
    setEditingTenant(tenant);
    setTenantEditError(null);
  };

  const handleUpdateTenant = async (e: React.FormEvent) => {
    e.preventDefault();
    setTenantEditLoading(true);
    setTenantEditError(null);
    try {
      const response = await updateTenant(editingTenant.id, editingTenant);
      const updated = response.data;
      setTenants(prev => prev.map(t => t.id === updated.id ? updated : t));
      setEditingTenant(null);
    } catch (err) {
      setTenantEditError('Failed to update tenant');
    } finally {
      setTenantEditLoading(false);
    }
  };

  const handleDeleteTenant = async (id: number) => {
    if (!window.confirm('Are you sure you want to delete this tenant?')) return;
    try {
      await deleteTenant(id);
      setTenants(prev => prev.filter(t => t.id !== id));
    } catch {
      alert('Failed to delete tenant');
    }
  };

  const handleAddTenant = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const newTenant = await createTenant({
        first_name: tenantFirstName,
        last_name: tenantLastName,
        email: tenantEmail,
        phone: tenantPhone,
        property: tenantProperty,
      });
      setTenants(prev => [...prev, newTenant]);
      alert('Tenant added successfully!');
      setShowAddTenant(false);
      setTenantFirstName('');
      setTenantLastName('');
      setTenantEmail('');
      setTenantPhone('');
      setTenantProperty('');
    } catch (err) {
      alert('Error adding tenant');
    }
  };

  return (
    <div className="page">
      <h2>Tenants</h2>
      <button className="btn btn-primary" onClick={() => setShowAddTenant(true)}>
        + Add Tenant
      </button>
      <div className="tenant-list">
        {tenants.length === 0 ? (
          <div className="empty-state">No tenants found.</div>
        ) : (
          tenants.map((tenant, idx) => (
            <div className="tenant-card" key={idx}>
              <h3>{tenant.first_name} {tenant.last_name}</h3>
              <p>Property: {tenant.property}</p>
              <p>Email: {tenant.email}</p>
              <p>Phone: {tenant.phone}</p>
              <button onClick={() => handleEditTenant(tenant)}>Edit</button>
              <button onClick={() => handleDeleteTenant(tenant.id)}>Delete</button>
            </div>
          ))
        )}
      </div>
      {showAddTenant && (
        <div className="modal-overlay">
          <div className="modal">
            <div className="modal-header">
              <h3>Add New Tenant</h3>
              <button className="modal-close" onClick={() => setShowAddTenant(false)}>×</button>
            </div>
            <div className="modal-body">
              <form className="property-form" onSubmit={handleAddTenant}>
                <div className="form-group">
                  <label>First Name:</label>
                  <input type="text" value={tenantFirstName} onChange={e => setTenantFirstName(e.target.value)} required />
                </div>
                <div className="form-group">
                  <label>Last Name:</label>
                  <input type="text" value={tenantLastName} onChange={e => setTenantLastName(e.target.value)} required />
                </div>
                <div className="form-group">
                  <label>Email:</label>
                  <input type="email" value={tenantEmail} onChange={e => setTenantEmail(e.target.value)} required />
                </div>
                <div className="form-group">
                  <label>Phone:</label>
                  <input type="text" value={tenantPhone} onChange={e => setTenantPhone(e.target.value)} required />
                </div>
                <div className="form-group">
                  <label>Property Renting:</label>
                  <select value={tenantProperty} onChange={e => setTenantProperty(e.target.value)} required>
                    <option value="">Select Property</option>
                    {properties.map((property: any) => (
                      <option key={property.id} value={property.name}>{property.name}</option>
                    ))}
                  </select>
                </div>
                <div className="form-actions">
                  <button type="button" className="btn btn-secondary" onClick={() => setShowAddTenant(false)}>
                    Cancel
                  </button>
                  <button type="submit" className="btn btn-primary">
                    Add Tenant
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}

      {/* Edit Tenant Modal */}
      {editingTenant && (
        <div className="modal-overlay">
          <div className="modal">
            <div className="modal-header">
              <h3>Edit Tenant</h3>
              <button className="modal-close" onClick={() => setEditingTenant(null)}>×</button>
            </div>
            <div className="modal-body">
              <form className="property-form" onSubmit={handleUpdateTenant}>
                <div className="form-group">
                  <label>First Name:</label>
                  <input type="text" value={editingTenant.first_name} onChange={e => setEditingTenant({ ...editingTenant, first_name: e.target.value })} />
                </div>
                <div className="form-group">
                  <label>Last Name:</label>
                  <input type="text" value={editingTenant.last_name} onChange={e => setEditingTenant({ ...editingTenant, last_name: e.target.value })} />
                </div>
                <div className="form-group">
                  <label>Email:</label>
                  <input type="email" value={editingTenant.email} onChange={e => setEditingTenant({ ...editingTenant, email: e.target.value })} />
                </div>
                <div className="form-group">
                  <label>Phone:</label>
                  <input type="text" value={editingTenant.phone} onChange={e => setEditingTenant({ ...editingTenant, phone: e.target.value })} />
                </div>
                <div className="form-group">
                  <label>Property:</label>
                  <select value={editingTenant.property} onChange={e => setEditingTenant({ ...editingTenant, property: e.target.value })}>
                    <option value="">Select Property</option>
                    {properties.map((property: any) => (
                      <option key={property.id} value={property.name}>{property.name}</option>
                    ))}
                  </select>
                </div>
                <div className="form-actions">
                  <button type="button" className="btn btn-secondary" onClick={() => setEditingTenant(null)}>
                    Cancel
                  </button>
                  <button type="submit" className="btn btn-primary" disabled={tenantEditLoading}>
                    {tenantEditLoading ? 'Updating...' : 'Update Tenant'}
                  </button>
                </div>
                {tenantEditError && <div style={{ color: 'red' }}>{tenantEditError}</div>}
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

const Documents = () => (
  <div className="page">
    <h2>Documents</h2>
    <div className="document-list">
      <div className="document-card">
        <h3>Lease Agreement - 123 Main St</h3>
        <p>Signed: January 15, 2024</p>
        <button className="btn">View PDF</button>
      </div>
      <div className="document-card">
        <h3>Property Insurance</h3>
        <p>Expires: December 31, 2024</p>
        <button className="btn">View PDF</button>
      </div>
    </div>
  </div>
);

const App: React.FC = () => {
  const [locations, setLocations] = useState<string[]>([]);
  const [properties, setProperties] = useState<any[]>([]);
  const [tenants, setTenants] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true);
    Promise.all([fetchProperties(), fetchTenants()])
      .then(([props, tens]) => {
        setProperties(props);
        setTenants(tens);
        // Derive locations from properties
        const uniqueLocations = Array.from(new Set(props.map((p: any) => p.city).filter(Boolean))) as string[];
        setLocations(uniqueLocations);
        setLoading(false);
      })
      .catch((err) => {
        setError('Failed to load data from backend');
        setLoading(false);
      });
  }, []);

  return (
    <Router>
      <div className="app">
        <nav className="navbar">
          <div className="nav-brand">
            <h1>Property Management</h1>
          </div>
          <ul className="nav-links">
            <li><Link to="/">Dashboard</Link></li>
            <li><Link to="/properties">Properties</Link></li>
            <li><Link to="/tenants">Tenants</Link></li>
            <li><Link to="/documents">Documents</Link></li>
          </ul>
        </nav>
        
        <main className="main-content">
          {loading ? (
            <div>Loading...</div>
          ) : error ? (
            <div style={{ color: 'red' }}>{error}</div>
          ) : (
            <Routes>
              <Route path="/" element={<Dashboard properties={properties} setProperties={setProperties} locations={locations} setLocations={setLocations} createPropertyWithTenant={createPropertyWithTenant} />} />
              <Route path="/properties" element={<Properties properties={properties} setProperties={setProperties} locations={locations} setLocations={setLocations} createPropertyWithTenant={createPropertyWithTenant} />} />
              <Route path="/tenants" element={<Tenants properties={properties} tenants={tenants} setTenants={setTenants} createTenant={createTenant} />} />
              <Route path="/documents" element={<Documents />} />
              <Route path="*" element={<div className="page"><h2>Page Not Found</h2><p>The page you're looking for doesn't exist.</p></div>} />
            </Routes>
          )}
        </main>
      </div>
    </Router>
  );
};

export default App;
