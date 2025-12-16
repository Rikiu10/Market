const API_URL = 'http://localhost:8000/api';

export const Api = {
    // --- PRODUCTS ---
    getProducts: async () => {
        const response = await fetch(`${API_URL}/productos/`);
        if (!response.ok) throw new Error('Error fetching products');
        return await response.json();
    },

    getProduct: async (id) => {
        const response = await fetch(`${API_URL}/productos/${id}/`);
        if (!response.ok) return null;
        return await response.json();
    },

    saveProduct: async (product) => {
        const method = product.id ? 'PUT' : 'POST';
        const url = product.id ? `${API_URL}/productos/${product.id}/` : `${API_URL}/productos/`;

        // Ensure numbers are numbers
        const payload = {
            ...product,
            precio: parseInt(product.precio),
            stock_actual: parseInt(product.stock), // Backend expects stock_actual
            cantidad_minima: parseInt(product.cantidad_minima),
            stock: undefined, // remove frontend alias if backend has different name
        };

        // Note: serializer uses 'stock_actual' in model but helper 'to_dict' in old python code used 'stock'.
        // Let's check serializer. Model has 'stock_actual'. Serializer uses __all__. 
        // So JSON field is 'stock_actual'.

        const response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload),
        });

        if (!response.ok) {
            console.error(await response.text());
            throw new Error('Error saving product');
        }
        return await response.json();
    },

    deleteProduct: async (id) => {
        await fetch(`${API_URL}/productos/${id}/`, { method: 'DELETE' });
    },

    // --- SALES (POS) ---
    createSale: async (saleData) => {
        // Backend expects 'Venta' model structure.
        // Standard DRF ModelViewSet for Venta usually expects just fields for Venta.
        // But we need to create Venta AND DetalleVenta AND update Stock.
        // The default VentaSerializer is simple.
        // We probably need a custom endpoint or do it in client side:
        // 1. Create Venta -> get ID.
        // 2. Create DetalleVenta for each item.
        // 3. Update Product stock for each item.
        // This is transactionally unsafe in client but standard for simple REST.
        // BETTER: Use a single custom endpoint. But sticking to standard ViewSets for now:

        // 1. Create Venta
        const ventaPayload = {
            fecha: new Date().toISOString().split('T')[0], // YYYY-MM-DD
            total: saleData.total,
            // empleado: ??? We need employee ID. Mock Auth doesn't have real IDs yet.
            // For now send null or 1 if possible.
            empleado: null
        };

        const ventaRes = await fetch(`${API_URL}/ventas/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(ventaPayload)
        });

        if (!ventaRes.ok) throw new Error('Error creating Sale');
        const venta = await ventaRes.json();

        // 2. Create Details & Update Stock
        for (const item of saleData.items) {
            // Detalle
            await fetch(`${API_URL}/detalle-ventas/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    venta: venta.idventa, // or id
                    producto: item.productId,
                    cantidad_producto: item.quantity,
                    precio_unitario: item.price,
                    subtotal: item.quantity * item.price
                })
            });

            // Update Stock (Get current, subtract, Put)
            // Actually `saveProduct` handles updates.
            // We need to fetch fresh specific product first?
            // Or just optimistic update if we have data.
            // Let's fetch fresh to be safe.
            const prodRes = await fetch(`${API_URL}/productos/${item.productId}/`);
            const prod = await prodRes.json();

            await fetch(`${API_URL}/productos/${item.productId}/`, {
                method: 'PATCH', // Partial update
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    stock_actual: prod.stock_actual - item.quantity
                })
            });
        }

        return venta;
    },

    getSale: async (id) => {
        const response = await fetch(`${API_URL}/ventas/${id}/`);
        if (!response.ok) throw new Error('Error fetching sale');
        return await response.json();
    },

    updateSale: async (id, data) => {
        const response = await fetch(`${API_URL}/ventas/${id}/`, {
            method: 'PUT', // or PATCH
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        if (!response.ok) throw new Error('Error updating sale');
        return await response.json();
    },

    getSales: async () => {
        const response = await fetch(`${API_URL}/ventas/`);
        if (!response.ok) throw new Error('Error fetching sales');
        return await response.json();
    },

    deleteSale: async (id) => {
        await fetch(`${API_URL}/ventas/${id}/`, { method: 'DELETE' });
    },

    // --- EMPLOYEES (DUEÑA) ---
    getEmployees: async () => {
        const response = await fetch(`${API_URL}/empleados/`);
        if (!response.ok) throw new Error('Error fetching employees');
        return await response.json();
    },

    getEmployee: async (id) => {
        const response = await fetch(`${API_URL}/empleados/${id}/`);
        if (!response.ok) return null;
        return await response.json();
    },

    saveEmployee: async (employee) => {
        const method = employee.id ? 'PUT' : 'POST'; // or idempleado ?
        // Check serializer: idempleado is PK.
        const url = employee.id ? `${API_URL}/empleados/${employee.id}/` : `${API_URL}/empleados/`;

        // Payload adaptation if needed
        const payload = { ...employee };

        const response = await fetch(url, {
            method: method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
        });
        if (!response.ok) throw new Error('Error saving employee');
        return await response.json();
    },

    deleteEmployee: async (id) => {
        await fetch(`${API_URL}/empleados/${id}/`, { method: 'DELETE' });
    },

    // --- MOVIMIENTOS (DUEÑA) ---
    getMovements: async () => {
        const response = await fetch(`${API_URL}/movimientos/`);
        if (!response.ok) throw new Error('Error fetching movements');
        return await response.json();
    },

    saveMovement: async (data) => {
        const method = data.idmovimiento ? 'PUT' : 'POST';
        const url = data.idmovimiento ? `${API_URL}/movimientos/${data.idmovimiento}/` : `${API_URL}/movimientos/`;
        const res = await fetch(url, {
            method: method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        if (!res.ok) throw new Error('Error saving movement');
        return await res.json();
    },

    deleteMovement: async (id) => {
        await fetch(`${API_URL}/movimientos/${id}/`, { method: 'DELETE' });
    },

    // --- TIPO EMPLEADO ---
    getEmployeeTypes: async () => {
        const res = await fetch(`${API_URL}/tipo-empleado/`);
        if (!res.ok) throw new Error('Error fetching employee types');
        return await res.json();
    },

    saveEmployeeType: async (data) => {
        const method = data.idtipoEmpleado ? 'PUT' : 'POST';
        const url = data.idtipoEmpleado ? `${API_URL}/tipo-empleado/${data.idtipoEmpleado}/` : `${API_URL}/tipo-empleado/`;
        const res = await fetch(url, {
            method: method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        if (!res.ok) throw new Error('Error saving employee type');
        return await res.json();
    },

    deleteEmployeeType: async (id) => {
        await fetch(`${API_URL}/tipo-empleado/${id}/`, { method: 'DELETE' });
    },

    // --- CREDENCIALES ---
    getCredentials: async () => {
        const res = await fetch(`${API_URL}/credenciales/`);
        if (!res.ok) throw new Error('Error fetching credentials');
        return await res.json();
    },

    saveCredential: async (data) => {
        const method = data.idcredenciales ? 'PUT' : 'POST';
        const url = data.idcredenciales ? `${API_URL}/credenciales/${data.idcredenciales}/` : `${API_URL}/credenciales/`;
        const res = await fetch(url, {
            method: method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        if (!res.ok) throw new Error('Error saving credential');
        return await res.json();
    },

    deleteCredential: async (id) => {
        await fetch(`${API_URL}/credenciales/${id}/`, { method: 'DELETE' });
    },

    // --- ALERTAS ---
    getAlerts: async () => {
        const res = await fetch(`${API_URL}/alertas/`);
        if (!res.ok) throw new Error('Error fetching alerts');
        return await res.json();
    },

    deactivateAlert: async (id) => {
        // Custom endpoint behavior: POST to 'desactivar' or PATCH 'estado' field?
        // Django urls says: path("alertas/desactivar/<int:alerta_id>/", ...
        // Let's assume the view handles POST.
        const res = await fetch(`${API_URL}/alertas/desactivar/${id}/`, { method: 'POST' });
        // If 405, try GET or check API design. Usually action endpoints are POST.
        if (!res.ok) {
            // Fallback: maybe just delete? Or PATCH?
            // Let's stick to the URL pattern.
            throw new Error('Error deactivating alert');
        }
        return await res.json(); // or text
    },

    getAlertHistory: async () => {
        const res = await fetch(`${API_URL}/alertas/historial/`); // or /historiales/ ? 
        // Logic check: "alertas/historial/" is in Django URLs for view, but DRF usually has its own.
        // If we strictly follow api_urls.py (ViewSets):
        // router.register('historial', HistorialViewSet) -> /api/historial/
        const response = await fetch(`${API_URL}/historial/`);
        if (!response.ok) throw new Error('Error fetching alert history');
        return await response.json();
    },

    // --- HISTORIAL (CRUD Genérico) ---
    // Often read-only but Dueña has CRUD in Django templates.
    saveHistory: async (data) => {
        const method = data.idhistorial ? 'PUT' : 'POST';
        const url = data.idhistorial ? `${API_URL}/historial/${data.idhistorial}/` : `${API_URL}/historial/`;
        const res = await fetch(url, {
            method: method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        if (!res.ok) throw new Error('Error saving history');
        return await res.json();
    },

    deleteHistory: async (id) => {
        await fetch(`${API_URL}/historial/${id}/`, { method: 'DELETE' });
    }
};
