import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { Api } from '../../services/api';

const CredencialForm = () => {
    const { id } = useParams();
    const navigate = useNavigate();
    const [formData, setFormData] = useState({ user: '', password: '' });

    useEffect(() => {
        if (id) {
            const load = async () => {
                const list = await Api.getCredentials();
                const item = list.find(c => c.idcredenciales.toString() === id);
                if (item) setFormData({ user: item.user, password: item.password });
            };
            load();
        }
    }, [id]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await Api.saveCredential({ idcredenciales: id, ...formData });
            navigate('/credenciales');
        } catch (error) {
            alert('Error al guardar. Verifica que el usuario no exista.');
        }
    };

    return (
        <div className="container mt-4">
            <h2>{id ? 'Editar' : 'Nueva'} Credencial</h2>
            <div className="card shadow-sm p-4 mt-3" style={{ maxWidth: '500px' }}>
                <form onSubmit={handleSubmit}>
                    <div className="mb-3">
                        <label className="form-label">Usuario</label>
                        <input
                            type="text"
                            className="form-control"
                            value={formData.user}
                            onChange={e => setFormData({ ...formData, user: e.target.value })}
                            required
                        />
                    </div>
                    <div className="mb-3">
                        <label className="form-label">Password</label>
                        <input
                            type="text"
                            className="form-control"
                            value={formData.password}
                            onChange={e => setFormData({ ...formData, password: e.target.value })}
                            required
                        />
                    </div>
                    <button type="submit" className="btn btn-success me-2">Guardar</button>
                    <button type="button" className="btn btn-secondary" onClick={() => navigate('/credenciales')}>Cancelar</button>
                </form>
            </div>
        </div>
    );
};

export default CredencialForm;
