import React from "react";
import { Link } from "react-router-dom";
import { Button } from "semantic-ui-react";

export function Home() {
  return (
    <div style={{ padding: "48px", textAlign: "center" }}>
      <h1>Home Page — Tienda Online</h1>
      <p>Bienvenido al portal de clientes de Tienda Online.</p>
      <div style={{ marginTop: "20px", display: "flex", gap: "12px", justifyContent: "center" }}>
        <Button as={Link} to="/login" primary>
          Ir a Login
        </Button>
        <Button as={Link} to="/register" secondary>
          Registrarse
        </Button>
        <Button as={Link} to="/dashboard" color="teal">
          Ir al Dashboard
        </Button>
      </div>
    </div>
  );
}
