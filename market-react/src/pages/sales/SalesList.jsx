import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Api } from '../../services/api';

const SalesList = () => {
    const [sales, setSales] = useState([]);
    const navigate = useNavigate();

    useEffect(() => {
        const loadSales = async () => {
            try {
                const data = await Api.getSales();
                setSales(data);
            } catch (error) {
                console.error("Error loading sales:", error);
            }
        };
        loadSales();
    }, []);

    return (
        <div className="container mt-4">
            <h2 className="mb-4">Historial de Ventas</h2>

            <div className="table-responsive">
                <table className="table table-striped table-hover shadow-sm">
                    <thead className="table-success">
                        <tr>
                            <th>ID Venta</th>
                            <th>Fecha</th>
                            <th>Total</th>
                            <th>Detalles</th>
                            <th>Acciones</th>
                        </tr>
                    </thead>
                    <tbody>
                        {sales.length === 0 ? (
                            <tr>
                                <td colSpan="5" className="text-center">No hay ventas registradas.</td>
                            </tr>
                        ) : (
                            sales.map((sale) => (
                                <tr key={sale.idventa}>
                                    <td>#{sale.idventa}</td>
                                    <td>{sale.fecha}</td>
                                    <td>${sale.total}</td>
                                    <td>
                                        {/* Simple visualization of details if available in serializer */}
                                        {sale.detalles && sale.detalles.length > 0 ? (
                                            <ul className="list-unstyled mb-0 small">
                                                {sale.detalles.map(d => (
                                                    <li key={d.iddetalle_venta}>
                                                        Prod ID: {d.producto} x {d.cantidad_producto}
                                                    </li>
                                                ))}
                                            </ul>
                                        ) : (
                                            <span className="text-muted">Ver detalles</span>
                                        )}
                                    </td>
                                    <td>
                                        <button
                                            className="btn btn-sm btn-outline-primary me-2"
                                            onClick={() => navigate(`/ventas/editar/${sale.idventa}`)}
                                        >
                                            <i className="bi bi-pencil"></i> Editar
                                        </button>
                                        <button
                                            className="btn btn-sm btn-outline-danger"
                                            onClick={async () => {
                                                if (window.confirm('¿Eliminar esta venta?')) {
                                                    try {
                                                        await Api.deleteSale(sale.idventa);
                                                        setSales(sales.filter(s => s.idventa !== sale.idventa));
                                                    } catch (e) {
                                                        alert('Error al eliminar');
                                                    }
                                                }
                                            }}
                                        >
                                            <i className="bi bi-trash"></i> Eliminar
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

export default SalesList;
