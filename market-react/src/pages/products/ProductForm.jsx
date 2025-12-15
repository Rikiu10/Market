import React, { useState, useEffect } from 'react';
import { useNavigate, useParams, Link } from 'react-router-dom';
import { Api } from '../../services/api';

const ProductForm = () => {
    const { id } = useParams();
    const navigate = useNavigate();

    const [formData, setFormData] = useState({
        nombre: '',
        descripcion: '',
        precio: '',
        stock: '', // Maps to stock_actual
        cantidad_minima: ''
    });

    useEffect(() => {
        const loadProduct = async () => {
            if (id) {
                try {
                    const product = await Api.getProduct(id);
                    if (product) {
                        setFormData({
                            id: product.idproducto, // Use DB Primary Key
                            nombre: product.nombre,
                            descripcion: product.descripcion,
                            precio: product.precio,
                            stock: product.stock_actual, // Backend field name
                            cantidad_minima: product.cantidad_minima
                        });
                    }
                } catch (error) {
                    console.error("Error loading product:", error);
                }
            }
        };
        loadProduct();
    }, [id]);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await Api.saveProduct(formData);
            navigate('/productos');
        } catch (error) {
            alert('Error al guardar el producto');
        }
    };

    return (
        <div className="container mt-4">
            <div className="card shadow-sm" style={{ maxWidth: '600px', margin: '0 auto' }}>
                <div className="card-header bg-primary text-white">
                    <h4 className="mb-0">{id ? 'Editar Producto' : 'Nuevo Producto'}</h4>
                </div>
                <div className="card-body">
                    <form onSubmit={handleSubmit}>
                        <div className="mb-3">
                            <label className="form-label">Nombre</label>
                            <input
                                type="text" name="nombre"
                                className="form-control" required
                                value={formData.nombre} onChange={handleChange}
                            />
                        </div>

                        <div className="mb-3">
                            <label className="form-label">Descripción</label>
                            <textarea
                                name="descripcion" rows="2"
                                className="form-control"
                                value={formData.descripcion} onChange={handleChange}
                            ></textarea>
                        </div>

                        <div className="row">
                            <div className="col-md-4 mb-3">
                                <label className="form-label">Precio</label>
                                <input
                                    type="number" name="precio"
                                    className="form-control" required min="0"
                                    value={formData.precio} onChange={handleChange}
                                />
                            </div>
                            <div className="col-md-4 mb-3">
                                <label className="form-label">Stock Actual</label>
                                <input
                                    type="number" name="stock"
                                    className="form-control" required min="0"
                                    value={formData.stock} onChange={handleChange}
                                />
                            </div>
                            <div className="col-md-4 mb-3">
                                <label className="form-label">Stock Mínimo</label>
                                <input
                                    type="number" name="cantidad_minima"
                                    className="form-control" required min="0"
                                    value={formData.cantidad_minima} onChange={handleChange}
                                />
                            </div>
                        </div>

                        <div className="d-flex justify-content-end gap-2 mt-3">
                            <Link to="/productos" className="btn btn-secondary">Cancelar</Link>
                            <button type="submit" className="btn btn-success">Guardar</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    );
};

export default ProductForm;
