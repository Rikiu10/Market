import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { Api } from '../../services/api';

const TipoEmpleadoForm = () => {
    const { id } = useParams();
    const navigate = useNavigate();
    const [rol, setRol] = useState('');

    useEffect(() => {
        if (id) {
            const load = async () => {
                const types = await Api.getEmployeeTypes();
                const item = types.find(t => t.idtipoEmpleado.toString() === id);
                if (item) setRol(item.rol);
            };
            load();
        }
    }, [id]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await Api.saveEmployeeType({ idtipoEmpleado: id, rol });
            navigate('/tipoempleados');
        } catch (error) {
            alert('Error al guardar');
        }
    };

    return (
        <div className="container mt-4">
            <h2>{id ? 'Editar' : 'Nuevo'} Tipo de Empleado</h2>
            <div className="card shadow-sm p-4 mt-3" style={{ maxWidth: '500px' }}>
                <form onSubmit={handleSubmit}>
                    <div className="mb-3">
                        <label className="form-label">Rol</label>
                        <input
                            type="text"
                            className="form-control"
                            value={rol}
                            onChange={e => setRol(e.target.value)}
                            required
                        />
                    </div>
                    <button type="submit" className="btn btn-success me-2">Guardar</button>
                    <button type="button" className="btn btn-secondary" onClick={() => navigate('/tipoempleados')}>Cancelar</button>
                </form>
            </div>
        </div>
    );
};

export default TipoEmpleadoForm;
