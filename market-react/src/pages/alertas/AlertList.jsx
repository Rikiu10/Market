import React, { useState, useEffect } from 'react';
import { Api } from '../../services/api';

const AlertList = () => {
    const [alerts, setAlerts] = useState([]);

    const loadAlerts = async () => {
        try {
            const data = await Api.getAlerts();
            setAlerts(data);
        } catch (error) {
            console.error(error);
        }
    };

    useEffect(() => { loadAlerts(); }, []);

    const handleDeactivate = async (id) => {
        if (window.confirm('¿Desactivar esta alerta?')) {
            try {
                await Api.deactivateAlert(id);
                loadAlerts(); // Refresh list to see status change
            } catch (error) {
                alert('Error al desactivar alerta');
            }
        }
    };

    return (
        <div className="container mt-4">
            <h2 className="mb-4">Alertas de Stock</h2>

            <div className="table-responsive">
                <table className="table table-bordered shadow-sm bg-white">
                    <thead className="table-danger">
                        <tr>
                            <th>ID</th>
                            <th>Descripción</th>
                            <th>Estado</th>
                            <th>Acciones</th>
                        </tr>
                    </thead>
                    <tbody>
                        {alerts.length === 0 ? (
                            <tr><td colSpan="4" className="text-center">No hay alertas.</td></tr>
                        ) : (
                            alerts.map(a => (
                                <tr key={a.idalerta || a.id}>
                                    <td>{a.idalerta || a.id}</td>
                                    <td>{a.descripcion}</td>
                                    <td>
                                        <span className={`badge ${a.estado === 'ACTIVA' ? 'bg-danger' : 'bg-secondary'}`}>
                                            {a.estado}
                                        </span>
                                    </td>
                                    <td>
                                        {a.estado === 'ACTIVA' && (
                                            <button className="btn btn-sm btn-outline-dark"
                                                onClick={() => handleDeactivate(a.idalerta || a.id)}>
                                                Desactivar
                                            </button>
                                        )}
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

export default AlertList;
