const API_URL = import.meta.env.VITE_BASE_API_URL || "http://localhost:8000";

export async function loginApi(formData) {
  try {
    const url = `${API_URL}/api/v1/auth/token/`;
    console.log("url", url);
    const params = {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(formData),
    };
    const response = await fetch(url, params);
    if (response.status !== 200) {
      throw new Error("Usuario o contraseña incorrecta");
    }
    const result = await response.json();
    return result;
  } catch (error) {
    throw new Error(error.message || "Error al iniciar sesión");
  }
}

export async function registerApi(formData) {
  try {
    const url = `${API_URL}/api/v1/auth/register/`;
    console.log("url", url);
    const params = {
      method: "POST",
      headers: {
        accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify(formData),
    };
    const response = await fetch(url, params);
    if (response.status !== 201) {
      throw new Error("No se puede crear el usuario");
    }
    const result = await response.json();
    return result;
  } catch (error) {
    throw new Error(error.message || "Error al registrar usuario");
  }
}

export async function getMeApi(token) {
  try {
    const url = `${API_URL}/api/v1/auth/me/`;
    const params = {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    };
    const response = await fetch(url, params);
    const result = await response.json();
    return result;
  } catch (error) {
    throw error;
  }
}

export async function getSoapCountryApi(codigo = "MX") {
  const url = `${API_URL}/api/v1/soap/pais/?codigo=${codigo}`;
  const response = await fetch(url);
  return await response.json();
}
