import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { Api } from '../../services/api';

const EmployeeForm = () => {
    const { id } = useParams();
    const navigate = useNavigate();

    // Dropdown data
    const [credentials, setCredentials] = useState([]);
    const [types, setTypes] = useState([]);

    const [formData, setFormData] = useState({
        legajo: '', // generated or manual? Django Form didn't start with it, but Model has it. Let's assume manual or backend gen.
        nombre: '',
        apellido: '',
        email: '',
        telefono: '',
        credenciales: '', // ID
        tipoEmpleado: ''  // ID
    });

    useEffect(() => {
        const loadDependencies = async () => {
            try {
                const [creds, roles] = await Promise.all([
                    Api.getCredentials(),
                    Api.getEmployeeTypes()
                ]);
                setCredentials(creds);
                setTypes(roles);

                if (id) {
                    const emp = await Api.getEmployee(id);
                    if (emp) {
                        setFormData({
                            legajo: emp.legajo || '',
                            nombre: emp.nombre,
                            apellido: emp.apellido,
                            email: emp.email,
                            telefono: emp.telefono || '',
                            credenciales: emp.credenciales,
                            tipoEmpleado: emp.tipoEmpleado || emp.tipo_empleado_id // Check serializer field name for ID
                        });
                    }
                }
            } catch (error) {
                console.error("Error loading data", error);
            }
        };
        loadDependencies();
    }, [id]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await Api.saveEmployee({ idempleado: id, ...formData });
            alert('Empleado guardado correctamente');
            navigate('/empleados');
        } catch (error) {
            alert('Error al guardar empleado');
        }
    };

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    return (
        <div className="container mt-4">
            <h2>{id ? 'Editar' : 'Nuevo'} Empleado</h2>
            <div className="card shadow-sm p-4 mt-3">
                <form onSubmit={handleSubmit}>
                    <div className="row">
                        <div className="col-md-6 mb-3">
                            <label className="form-label">Nombre</label>
                            <input name="nombre" value={formData.nombre} onChange={handleChange} className="form-control" required />
                        </div>
                        <div className="col-md-6 mb-3">
                            <label className="form-label">Apellido</label>
                            <input name="apellido" value={formData.apellido} onChange={handleChange} className="form-control" required />
                        </div>
                    </div>

                    <div className="mb-3">
                        <label className="form-label">Email</label>
                        <input type="email" name="email" value={formData.email} onChange={handleChange} className="form-control" required />
                    </div>

                    <div className="mb-3">
                        <label className="form-label">Teléfono</label>
                        <input name="telefono" value={formData.telefono} onChange={handleChange} className="form-control" />
                    </div>

                    <div className="row">
                        <div className="col-md-6 mb-3">
                            <label className="form-label">Rol (Tipo Empleado)</label>
                            <select name="tipoEmpleado" value={formData.tipoEmpleado} onChange={handleChange} className="form-control" required>
                                <option value="">-- Seleccionar --</option>
                                {types.map(t => (
                                    <option key={t.idtipoEmpleado} value={t.idtipoEmpleado}>{t.rol}</option>
                                ))}
                            </select>
                            <div className="form-text"></div>
                        </div>

                        <div className="col-md-6 mb-3">
                            <label className="form-label">Credenciales (Usuario)</label>
                            <select name="credenciales" value={formData.credenciales} onChange={handleChange} className="form-control" required>
                                <option value="">-- Seleccionar --</option>
                                {credentials.map(c => (
                                    <option key={c.idcredenciales} value={c.idcredenciales}>{c.user}</option>
                                ))}
                            </select>
                            <div className="form-text"></div>
                        </div>
                    </div>

                    <button type="submit" className="btn btn-primary me-2">Guardar</button>
                    <button type="button" className="btn btn-secondary" onClick={() => navigate('/empleados')}>Cancelar</button>
                </form>
            </div>
        </div>
    );
};

export default EmployeeForm;
