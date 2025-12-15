import React, { useState, useEffect } from 'react';
import { Api } from '../../services/api';

const PointOfSale = () => {
    const [products, setProducts] = useState([]);
    const [cart, setCart] = useState([]);
    const [searchTerm, setSearchTerm] = useState('');
    const [total, setTotal] = useState(0);

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

    useEffect(() => {
        const newTotal = cart.reduce((acc, item) => acc + (item.precio * item.quantity), 0);
        setTotal(newTotal);
    }, [cart]);

    const addToCart = (product) => {
        if (product.stock_actual <= 0) {
            alert('Producto sin stock disponible');
            return;
        }

        const existingItem = cart.find(item => item.idproducto === product.idproducto);
        if (existingItem) {
            if (existingItem.quantity + 1 > product.stock_actual) {
                alert('No hay suficiente stock');
                return;
            }
            setCart(cart.map(item =>
                item.idproducto === product.idproducto ? { ...item, quantity: item.quantity + 1 } : item
            ));
        } else {
            setCart([...cart, { ...product, quantity: 1 }]);
        }
    };

    const removeFromCart = (productId) => {
        setCart(cart.filter(item => item.idproducto !== productId));
    };

    const updateQuantity = (productId, newQuantity) => {
        const product = products.find(p => p.idproducto === productId);
        if (newQuantity > product.stock_actual) {
            alert('Stock insuficiente');
            return;
        }
        if (newQuantity < 1) return;

        setCart(cart.map(item =>
            item.idproducto === productId ? { ...item, quantity: newQuantity } : item
        ));
    };

    const handleCheckout = async () => {
        if (cart.length === 0) return;

        if (window.confirm(`¿Confirmar venta por $${total}?`)) {
            const saleData = {
                total: total,
                items: cart.map(item => ({
                    productId: item.idproducto,
                    productName: item.nombre,
                    quantity: item.quantity,
                    price: item.precio
                }))
            };

            try {
                await Api.createSale(saleData);
                setCart([]);
                loadProducts(); // Refresh stock from backend
                alert('Venta realizada con éxito');
            } catch (error) {
                alert('Error al procesar la venta');
            }
        }
    };

    const filteredProducts = products.filter(p =>
        p.nombre.toLowerCase().includes(searchTerm.toLowerCase())
    );

    return (
        <div className="container mt-4">
            <h2 className="mb-4">Punto de Venta</h2>

            <div className="row">
                {/* Product Selection */}
                <div className="col-md-7">
                    <div className="card shadow-sm mb-3">
                        <div className="card-header bg-secondary text-white">
                            <input
                                type="text"
                                className="form-control"
                                placeholder="Buscar producto..."
                                value={searchTerm}
                                onChange={(e) => setSearchTerm(e.target.value)}
                            />
                        </div>
                        <div className="card-body" style={{ maxHeight: '600px', overflowY: 'auto' }}>
                            <div className="list-group">
                                {filteredProducts.map(product => (
                                    <button
                                        key={product.idproducto}
                                        className="list-group-item list-group-item-action d-flex justify-content-between align-items-center"
                                        onClick={() => addToCart(product)}
                                        disabled={product.stock_actual === 0}
                                    >
                                        <div>
                                            <h6 className="mb-0">{product.nombre}</h6>
                                            <small className="text-muted">Stock: {product.stock_actual}</small>
                                        </div>
                                        <span className="badge bg-primary rounded-pill">${product.precio}</span>
                                    </button>
                                ))}
                            </div>
                        </div>
                    </div>
                </div>

                {/* Cart */}
                <div className="col-md-5">
                    <div className="card shadow border-primary">
                        <div className="card-header bg-primary text-white">
                            <h5 className="mb-0">Carrito de Compras</h5>
                        </div>
                        <div className="card-body">
                            {cart.length === 0 ? (
                                <p className="text-center text-muted my-5">El carrito está vacío</p>
                            ) : (
                                <div className="table-responsive">
                                    <table className="table table-sm">
                                        <thead>
                                            <tr>
                                                <th>Prod</th>
                                                <th>Cant</th>
                                                <th>Subtotal</th>
                                                <th></th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {cart.map(item => (
                                                <tr key={item.idproducto}>
                                                    <td>{item.nombre}</td>
                                                    <td>
                                                        <input
                                                            type="number"
                                                            className="form-control form-control-sm"
                                                            style={{ width: '60px' }}
                                                            value={item.quantity}
                                                            onChange={(e) => updateQuantity(item.idproducto, parseInt(e.target.value))}
                                                        />
                                                    </td>
                                                    <td>${item.precio * item.quantity}</td>
                                                    <td>
                                                        <button
                                                            className="btn btn-sm btn-outline-danger"
                                                            onClick={() => removeFromCart(item.idproducto)}
                                                        >
                                                            &times;
                                                        </button>
                                                    </td>
                                                </tr>
                                            ))}
                                        </tbody>
                                    </table>
                                </div>
                            )}
                        </div>
                        <div className="card-footer">
                            <div className="d-flex justify-content-between align-items-center mb-3">
                                <h4>Total:</h4>
                                <h3 className="text-success">${total}</h3>
                            </div>
                            <button
                                className="btn btn-success w-100 btn-lg"
                                disabled={cart.length === 0}
                                onClick={handleCheckout}
                            >
                                Confirmar Venta
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default PointOfSale;
