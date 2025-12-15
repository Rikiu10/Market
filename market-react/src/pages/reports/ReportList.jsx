import React, { useState, useEffect } from 'react';
import { Api } from '../../services/api';

const ReportList = () => {
    const [stats, setStats] = useState({
        totalSales: 0,
        totalProducts: 0,
        totalRevenue: 0,
        lowStockCount: 0
    });

    useEffect(() => {
        const loadData = async () => {
            try {
                const [products, sales] = await Promise.all([
                    Api.getProducts(),
                    Api.getSales()
                ]);

                const totalRevenue = sales.reduce((acc, curr) => acc + parseFloat(curr.total), 0);
                const lowStock = products.filter(p => p.stock_actual <= p.cantidad_minima).length;

                setStats({
                    totalSales: sales.length,
                    totalProducts: products.length,
                    totalRevenue: totalRevenue,
                    lowStockCount: lowStock
                });
            } catch (error) {
                console.error("Error loading report data:", error);
            }
        };
        loadData();
    }, []);

    return (
        <div className="container mt-4">
            <h2 className="mb-4">Reportes Generales</h2>

            <div className="row g-4">
                <div className="col-md-3">
                    <div className="card text-white bg-primary h-100 shadow-sm">
                        <div className="card-body">
                            <h5 className="card-title">Ventas Totales</h5>
                            <h2 className="display-4 fw-bold">{stats.totalSales}</h2>
                            <p className="card-text">Transacciones registradas</p>
                        </div>
                    </div>
                </div>

                <div className="col-md-3">
                    <div className="card text-white bg-success h-100 shadow-sm">
                        <div className="card-body">
                            <h5 className="card-title">Ingresos</h5>
                            <h2 className="display-4 fw-bold">${stats.totalRevenue.toLocaleString()}</h2>
                            <p className="card-text">Total acumulado</p>
                        </div>
                    </div>
                </div>

                <div className="col-md-3">
                    <div className="card text-white bg-info h-100 shadow-sm">
                        <div className="card-body">
                            <h5 className="card-title">Productos</h5>
                            <h2 className="display-4 fw-bold">{stats.totalProducts}</h2>
                            <p className="card-text">En inventario</p>
                        </div>
                    </div>
                </div>

                <div className="col-md-3">
                    <div className="card text-white bg-danger h-100 shadow-sm">
                        <div className="card-body">
                            <h5 className="card-title">Stock Bajo</h5>
                            <h2 className="display-4 fw-bold">{stats.lowStockCount}</h2>
                            <p className="card-text">Productos bajo mínimo</p>
                        </div>
                    </div>
                </div>
            </div>

            <div className="mt-5">
                <h4>Gráficos</h4>
                <div className="alert alert-secondary">
                    <i className="bi bi-info-circle"></i> Los gráficos detallados se implementarán en una futura versión.
                </div>
            </div>
        </div>
    );
};

export default ReportList;
