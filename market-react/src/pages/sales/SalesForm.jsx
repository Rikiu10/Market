import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { Api } from '../../services/api';

const SalesForm = () => {
    const { id } = useParams();
    const navigate = useNavigate();
    const [employees, setEmployees] = useState([]);
    const [formData, setFormData] = useState({
        fecha: '',
        total: '',
        empleado: ''
    });

    useEffect(() => {
        const loadData = async () => {
            try {
                const empData = await Api.getEmployees();
                setEmployees(empData);

                if (id) {
                    const sale = await Api.getSale(id);
                    setFormData({
                        fecha: sale.fecha, // check format YYYY-MM-DD
                        total: sale.total,
                        empleado: sale.empleado || '' // might be ID or null
                    });
                }
            } catch (error) {
                console.error("Error loading form data", error);
            }
        };
        loadData();
    }, [id]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await Api.updateSale(id, formData);
            alert('Venta actualizada correctamente');
            navigate('/ventas');
        } catch (error) {
            console.error(error);
            alert('Error al actualizar venta');
        }
    };

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    return (
        <div className="container mt-4">
            <h2 className="mb-4">Editar Venta #{id}</h2>
            <div className="card shadow-sm">
                <div className="card-body">
                    <form onSubmit={handleSubmit}>
                        <div className="mb-3">
                            <label className="form-label">Fecha</label>
                            <input
                                type="date" // Django uses DateInput
                                name="fecha"
                                className="form-control"
                                value={formData.fecha}
                                onChange={handleChange}
                                required
                            />
                        </div>

                        <div className="mb-3">
                            <label className="form-label">Total</label>
                            <input
                                type="number"
                                name="total"
                                className="form-control"
                                value={formData.total}
                                onChange={handleChange}
                                required
                                min="0"
                            />
                            <div className="form-text text-warning">
                                <i className="bi bi-exclamation-triangle"></i> Cuidado: Modificar el total manualmente no recalcula los subtotales de los productos.
                            </div>
                        </div>

                        <div className="mb-3">
                            <label className="form-label">Empleado</label>
                            <select
                                name="empleado"
                                className="form-select"
                                value={formData.empleado}
                                onChange={handleChange}
                            >
                                <option value="">-- Seleccionar --</option>
                                {employees.map(e => (
                                    <option key={e.idempleado} value={e.idempleado}>
                                        {e.nombre} {e.apellido}
                                    </option>
                                ))}
                            </select>
                        </div>

                        <div className="d-flex gap-2">
                            <button type="submit" className="btn btn-primary">Guardar Cambios</button>
                            <button type="button" className="btn btn-secondary" onClick={() => navigate('/ventas')}>Cancelar</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    );
};

export default SalesForm;
