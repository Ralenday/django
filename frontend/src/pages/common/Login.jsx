import React from "react";
import { Button, Form } from "semantic-ui-react";
import { useFormik } from "formik";
import * as Yup from "yup";
import { toast } from "react-toastify";
import { loginApi } from "../../api/user";
import { useAuth } from "../../hooks/useAuth";
import { useNavigate, Link } from "react-router-dom";

export function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();

  const formik = useFormik({
    initialValues: initialValues(),
    validationSchema: validationSchema(),
    onSubmit: async (formValues) => {
      try {
        const response = await loginApi(formValues);
        const { access } = response;
        console.log("Token JWT obtenido:", access);
        await login(access);
        navigate("/dashboard");
      } catch (error) {
        toast.error(error.message);
      }
    },
  });

  return (
    <div className="login-admin">
      <div className="login-admin__content">
        <h1>Login</h1>
        <Form className="login-form-admin" onSubmit={formik.handleSubmit}>
          <label>Correo electrónico</label>
          <Form.Input
            name="email"
            placeholder="Correo electrónico"
            value={formik.values.email}
            onChange={formik.handleChange}
            onBlur={formik.handleBlur}
            error={formik.errors.email}
          />
          <label>Contraseña</label>
          <Form.Input
            name="password"
            type="password"
            placeholder="Contraseña"
            value={formik.values.password}
            onChange={formik.handleChange}
            error={formik.errors.password}
            autoComplete="false"
          />
          <Button type="submit" content="Iniciar Sesión" primary fluid />
          <div style={{ marginTop: "16px", textAlign: "center" }}>
            <Link to="/register">¿No tienes cuenta? Regístrate aquí</Link>
          </div>
        </Form>
      </div>
    </div>
  );
}

function initialValues() {
  return {
    email: "",
    password: "",
  };
}

function validationSchema() {
  return Yup.object({
    email: Yup.string()
      .email("Correo electrónico no válido")
      .required("El correo electrónico es obligatorio"),
    password: Yup.string().required("La contraseña es obligatoria"),
  });
}
