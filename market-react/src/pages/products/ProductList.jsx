import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Api } from '../../services/api';

const ProductList = () => {
    const [products, setProducts] = useState([]);

    const loadProducts = async () => {
        try {
            const data = await Api.getProducts();
            setProducts(data);
        } catch (error) {
            console.error(error);
        }
    };

    useEffect(() => {
        loadProducts();
    }, []);

    const handleDelete = async (id) => {
        if (window.confirm('¿Estás seguro de eliminar este producto?')) {
            await Api.deleteProduct(id);
            loadProducts();
        }
    };

    return (
        <div className="container mt-4">
            <div className="d-flex justify-content-between align-items-center mb-3">
                <h2>Inventario de Productos</h2>
                <Link to="/productos/nuevo" className="btn btn-primary">
                    <i className="bi bi-plus-lg"></i> Nuevo Producto
                </Link>
            </div>

            <div className="table-responsive">
                <table className="table table-striped table-hover shadow-sm">
                    <thead className="table-dark">
                        <tr>
                            <th>ID</th>
                            <th>Nombre</th>
                            <th>Precio</th>
                            <th>Stock</th>
                            <th>Min.</th>
                            <th>Acciones</th>
                        </tr>
                    </thead>
                    <tbody>
                        {products.length === 0 ? (
                            <tr>
                                <td colSpan="6" className="text-center">No hay productos registrados.</td>
                            </tr>
                        ) : (
                            products.map((p) => (
                                <tr key={p.idproducto}>
                                    <td>{p.idproducto}</td>
                                    <td>
                                        <strong>{p.nombre}</strong> <br />
                                        <small className="text-muted">{p.descripcion}</small>
                                    </td>
                                    <td>${p.precio}</td>
                                    <td className={p.stock_actual <= p.cantidad_minima ? 'text-danger fw-bold' : ''}>
                                        {p.stock_actual}
                                    </td>
                                    <td>{p.cantidad_minima}</td>
                                    <td>
                                        <Link to={`/productos/editar/${p.idproducto}`} className="btn btn-sm btn-warning me-2">
                                            Editar
                                        </Link>
                                        <button onClick={() => handleDelete(p.idproducto)} className="btn btn-sm btn-danger">
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

export default ProductList;
