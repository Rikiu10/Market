import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './services/auth';
import Layout from './components/Layout';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import ProductList from './pages/products/ProductList';
import ProductForm from './pages/products/ProductForm';
import PointOfSale from './pages/pos/PointOfSale';
import SalesList from './pages/sales/SalesList';
import SalesForm from './pages/sales/SalesForm';
import EmployeeList from './pages/employees/EmployeeList';
import EmployeeForm from './pages/employees/EmployeeForm';
import MovementList from './pages/movements/MovementList';
import MovementForm from './pages/movements/MovementForm';
import ReportList from './pages/reports/ReportList';
import HistorialList from './pages/historial/HistorialList';
import HistorialForm from './pages/historial/HistorialForm';
import AlertList from './pages/alertas/AlertList';
import TipoEmpleadoList from './pages/tipo_empleado/TipoEmpleadoList';
import TipoEmpleadoForm from './pages/tipo_empleado/TipoEmpleadoForm';
import CredencialesList from './pages/credenciales/CredencialesList';
import CredencialForm from './pages/credenciales/CredencialForm';

// Placeholder components for routes we haven't built yet
const Placeholder = ({ title }) => <div className="p-4"><h2>{title}</h2><p>Página en construcción</p></div>;

const ProtectedRoute = ({ children, roles }) => {
  const { user } = useAuth();
  if (!user) return <Navigate to="/login" replace />;
  if (roles && !roles.includes(user.role)) return <Navigate to="/" replace />;
  return children;
};

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Layout />}>
            <Route index element={<Dashboard />} />
            <Route path="login" element={<Login />} />

            {/* Gerente Routes */}
            <Route path="reportes" element={<ProtectedRoute roles={['GERENTE', 'JEFE']}><ReportList /></ProtectedRoute>} />
            <Route path="alertas" element={<ProtectedRoute roles={['GERENTE', 'JEFE']}><AlertList /></ProtectedRoute>} />

            {/* Shared Reports/Sales Routes */}
            <Route path="ventas" element={<ProtectedRoute roles={['GERENTE', 'JEFE', 'EMPLEADO']}><SalesList /></ProtectedRoute>} />
            <Route path="ventas/editar/:id" element={<ProtectedRoute roles={['GERENTE', 'JEFE', 'EMPLEADO']}><SalesForm /></ProtectedRoute>} />

            {/* Jefe Routes */}
            <Route path="productos" element={<ProtectedRoute roles={['JEFE']}><ProductList /></ProtectedRoute>} />
            <Route path="productos/nuevo" element={<ProtectedRoute roles={['JEFE']}><ProductForm /></ProtectedRoute>} />
            <Route path="productos/editar/:id" element={<ProtectedRoute roles={['JEFE']}><ProductForm /></ProtectedRoute>} />

            {/* Empleado Routes */}
            <Route path="pos" element={<ProtectedRoute roles={['EMPLEADO']}><PointOfSale /></ProtectedRoute>} />

            {/* Dueña Routes */}
            <Route path="empleados" element={<ProtectedRoute roles={['DUEÑA']}><EmployeeList /></ProtectedRoute>} />
            <Route path="empleados/nuevo" element={<ProtectedRoute roles={['DUEÑA']}><EmployeeForm /></ProtectedRoute>} />
            <Route path="empleados/editar/:id" element={<ProtectedRoute roles={['DUEÑA']}><EmployeeForm /></ProtectedRoute>} />

            {/* Credenciales */}
            <Route path="credenciales" element={<ProtectedRoute roles={['DUEÑA']}><CredencialesList /></ProtectedRoute>} />
            <Route path="credenciales/nueva" element={<ProtectedRoute roles={['DUEÑA']}><CredencialForm /></ProtectedRoute>} />
            <Route path="credenciales/editar/:id" element={<ProtectedRoute roles={['DUEÑA']}><CredencialForm /></ProtectedRoute>} />

            {/* Tipos de Empleado (agregado manually if not in base list, Dueña needs it) */}
            <Route path="tipoempleados" element={<ProtectedRoute roles={['DUEÑA']}><TipoEmpleadoList /></ProtectedRoute>} />
            <Route path="tipoempleados/nuevo" element={<ProtectedRoute roles={['DUEÑA']}><TipoEmpleadoForm /></ProtectedRoute>} />
            <Route path="tipoempleados/editar/:id" element={<ProtectedRoute roles={['DUEÑA']}><TipoEmpleadoForm /></ProtectedRoute>} />

            <Route path="movimientos" element={<ProtectedRoute roles={['DUEÑA']}><MovementList /></ProtectedRoute>} />
            <Route path="movimientos/nuevo" element={<ProtectedRoute roles={['DUEÑA']}><MovementForm /></ProtectedRoute>} />
            <Route path="movimientos/editar/:id" element={<ProtectedRoute roles={['DUEÑA']}><MovementForm /></ProtectedRoute>} />

            <Route path="historial" element={<ProtectedRoute roles={['DUEÑA']}><HistorialList /></ProtectedRoute>} />
            <Route path="historial/nuevo" element={<ProtectedRoute roles={['DUEÑA']}><HistorialForm /></ProtectedRoute>} />
            <Route path="historial/editar/:id" element={<ProtectedRoute roles={['DUEÑA']}><HistorialForm /></ProtectedRoute>} />

            <Route path="*" element={<Navigate to="/" replace />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
