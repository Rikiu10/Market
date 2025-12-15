import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Api } from '../../services/api';

const MovementList = () => {
    const [movements, setMovements] = useState([]);
    const navigate = useNavigate();

    const loadMovements = async () => {
        try {
            const data = await Api.getMovements();
            setMovements(data);
        } catch (error) {
            console.error("Error loading movements:", error);
        }
    };
    useEffect(() => {
        loadMovements();
    }, []);

    const handleDelete = async (id) => {
        if (window.confirm('¿Eliminar movimiento?')) {
            try {
                await Api.deleteMovement(id);
                loadMovements();
            } catch (error) {
                alert('Error al eliminar');
            }
        }
    };

    return (
        <div className="container mt-4">
            <div className="d-flex justify-content-between align-items-center mb-4">
                <h2>Movimientos de Stock</h2>
                <button className="btn btn-primary" onClick={() => navigate('/movimientos/nuevo')}>
                    Registrar Movimiento
                </button>
            </div>

            <div className="table-responsive">
                <table className="table table-bordered shadow-sm bg-white">
                    <thead className="table-secondary">
                        <tr>
                            <th>ID</th>
                            <th>Fecha</th>
                            <th>Producto</th>
                            <th>Tipo</th>
                            <th>Cantidad</th>
                            <th>Detalle</th>
                            <th>Acciones</th>
                        </tr>
                    </thead>
                    <tbody>
                        {movements.length === 0 ? (
                            <tr>
                                <td colSpan="6" className="text-center">No hay movimientos registrados.</td>
                            </tr>
                        ) : (
                            movements.map((m) => (
                                <tr key={m.idmovimiento}>
                                    <td>{m.idmovimiento}</td>
                                    <td>{m.fecha}</td>
                                    <td>{m.producto_nombre || m.producto}</td>
                                    <td>
                                        <span className={`badge ${m.tipo_movimiento === 'ENTRADA' ? 'bg-success' : 'bg-warning'}`}>
                                            {m.tipo_movimiento}
                                        </span>
                                    </td>
                                    <td>{m.cantidad}</td>
                                    <td>{m.descripcion}</td>
                                    <td>
                                        <button className="btn btn-sm btn-outline-primary me-2"
                                            onClick={() => navigate(`/movimientos/editar/${m.idmovimiento}`)}>
                                            Editar
                                        </button>
                                        <button className="btn btn-sm btn-outline-danger"
                                            onClick={() => handleDelete(m.idmovimiento)}>
                                            Eliminar
                                        </button>
                                    </td>
                                </tr>
                            ))
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default MovementList;
