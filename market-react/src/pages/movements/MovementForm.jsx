import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { Api } from '../../services/api';

const MovementForm = () => {
    const { id } = useParams();
    const navigate = useNavigate();
    const [products, setProducts] = useState([]);
    const [formData, setFormData] = useState({
        descripcion: '',
        fecha: '',
        tipo: 'ENTRADA', // Default
        producto: ''
    });

    useEffect(() => {
        const load = async () => {
            const prods = await Api.getProducts();
            setProducts(prods);

            if (id) {
                const moves = await Api.getMovements();
                const m = moves.find(item => item.idmovimiento.toString() === id);
                if (m) {
                    setFormData({
                        descripcion: m.descripcion,
                        fecha: m.fecha.replace('Z', ''), // Basic formatting if needed
                        tipo: m.tipo || m.tipo_movimiento,
                        producto: m.producto
                    });
                }
            }
        };
        load();
    }, [id]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await Api.saveMovement({ idmovimiento: id, ...formData });
            navigate('/movimientos');
        } catch (error) {
            alert('Error al guardar movimiento');
        }
    };

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    return (
        <div className="container mt-4">
            <h2>{id ? 'Editar' : 'Registrar'} Movimiento</h2>
            <div className="card shadow-sm p-4 mt-3" style={{ maxWidth: '600px' }}>
                <form onSubmit={handleSubmit}>
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
                        <label className="form-label">Tipo</label>
                        <select name="tipo" value={formData.tipo} onChange={handleChange} className="form-control" required>
                            <option value="ENTRADA">ENTRADA</option>
                            <option value="SALIDA">SALIDA</option>
                        </select>
                    </div>

                    <div className="mb-3">
                        <label className="form-label">Fecha</label>
                        <input type="datetime-local" name="fecha" value={formData.fecha} onChange={handleChange} className="form-control" required />
                    </div>

                    <div className="mb-3">
                        <label className="form-label">Descripción</label>
                        <textarea name="descripcion" value={formData.descripcion} onChange={handleChange} className="form-control" rows="3"></textarea>
                    </div>

                    <button type="submit" className="btn btn-primary me-2">Guardar</button>
                    <button type="button" className="btn btn-secondary" onClick={() => navigate('/movimientos')}>Cancelar</button>
                </form>
            </div>
        </div>
    );
};

export default MovementForm;
