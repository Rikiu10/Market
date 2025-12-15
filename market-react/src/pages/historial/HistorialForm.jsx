import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { Api } from '../../services/api';

const HistorialForm = () => {
    const { id } = useParams();
    const navigate = useNavigate();
    const [products, setProducts] = useState([]);
    const [alerts, setAlerts] = useState([]);

    const [formData, setFormData] = useState({
        fecha: '',
        alerta: '',
        producto: ''
    });

    useEffect(() => {
        const load = async () => {
            try {
                const [prods, als] = await Promise.all([
                    Api.getProducts(),
                    Api.getAlerts()
                ]);
                setProducts(prods);
                setAlerts(als);

                if (id) {
                    // Logic to fetch single history item could be added to API or filtered from list
                    // Let's assume filter from list for simplicity in this artifact
                    const list = await Api.getAlertHistory();
                    const item = list.find(h => h.idhistorial.toString() === id);
                    if (item) {
                        setFormData({
                            fecha: item.fecha.replace('Z', ''),
                            alerta: item.alerta,
                            producto: item.producto
                        });
                    }
                }
            } catch (error) {
                console.error(error);
            }
        };
        load();
    }, [id]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await Api.saveHistory({ idhistorial: id, ...formData });
            navigate('/historial');
        } catch (error) {
            alert('Error al guardar historial');
        }
    };

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    return (
        <div className="container mt-4">
            <h2>{id ? 'Editar' : 'Nuevo'} Historial</h2>
            <div className="card shadow-sm p-4 mt-3" style={{ maxWidth: '600px' }}>
                <form onSubmit={handleSubmit}>
                    <div className="mb-3">
                        <label className="form-label">Fecha</label>
                        <input type="datetime-local" name="fecha" value={formData.fecha} onChange={handleChange} className="form-control" required />
                    </div>

                    <div className="mb-3">
                        <label className="form-label">Producto</label>
                        <select name="producto" value={formData.producto} onChange={handleChange} className="form-control" required>
                            <option value="">-- Seleccionar --</option>
                            {products.map(p => (
                                <option key={p.id} value={p.id}>{p.nombre}</option>
                            ))}
                        </select>
                    </div>

                    <div className="mb-3">
                        <label className="form-label">Alerta Relacionada</label>
                        <select name="alerta" value={formData.alerta} onChange={handleChange} className="form-control" required>
                            <option value="">-- Seleccionar --</option>
                            {alerts.map(a => (
                                <option key={a.id} value={a.id}>#{a.id} - {a.descripcion}</option> // Assuming alert model structure
                            ))}
                        </select>
                    </div>

                    <button type="submit" className="btn btn-primary me-2">Guardar</button>
                    <button type="button" className="btn btn-secondary" onClick={() => navigate('/historial')}>Cancelar</button>
                </form>
            </div>
        </div>
    );
};

export default HistorialForm;
