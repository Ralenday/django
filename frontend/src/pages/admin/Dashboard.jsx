import React, { useEffect, useState } from "react";
import { Button, Icon, Label } from "semantic-ui-react";
import { useAuth } from "../../hooks/useAuth";
import { getSoapCountryApi } from "../../api/user";

export function Dashboard() {
  const { logout, auth } = useAuth();
  const user = auth?.me || {};

  // Estado para el widget de API de Terceros (Unidad 3)
  const [externalData, setExternalData] = useState({
    loading: true,
    usdMxn: "20.18",
    usdEur: "0.93",
    weatherTemp: "29.4 °C",
    weatherWind: "14 km/h",
    city: "San Luis Río Colorado, Son.",
    quote: "La calidad del software se construye capa por capa con buenas prácticas.",
    author: "Martin Fowler",
    sourceUrl: "https://open.er-api.com/v6/latest/USD & https://api.open-meteo.com/v1/forecast",
  });

  // Estado para mostrar la respuesta del servicio SOAP de Django (zeep)
  const [soapCountry, setSoapCountry] = useState(null);
  const [selectedIso, setSelectedIso] = useState("MX");

  const fetchThirdPartyApis = async () => {
    setExternalData((prev) => ({ ...prev, loading: true }));
    try {
      const [fxRes, weatherRes, quoteRes] = await Promise.allSettled([
        fetch("https://open.er-api.com/v6/latest/USD").then((r) => r.json()),
        fetch(
          "https://api.open-meteo.com/v1/forecast?latitude=32.45&longitude=-114.77&current_weather=true"
        ).then((r) => r.json()),
        fetch("https://dummyjson.com/quotes/random").then((r) => r.json()),
      ]);

      setExternalData((prev) => ({
        ...prev,
        loading: false,
        usdMxn:
          fxRes.status === "fulfilled" && fxRes.value?.rates?.MXN
            ? fxRes.value.rates.MXN.toFixed(2)
            : prev.usdMxn,
        usdEur:
          fxRes.status === "fulfilled" && fxRes.value?.rates?.EUR
            ? fxRes.value.rates.EUR.toFixed(2)
            : prev.usdEur,
        weatherTemp:
          weatherRes.status === "fulfilled" &&
          weatherRes.value?.current_weather?.temperature !== undefined
            ? `${weatherRes.value.current_weather.temperature} °C`
            : prev.weatherTemp,
        weatherWind:
          weatherRes.status === "fulfilled" &&
          weatherRes.value?.current_weather?.windspeed !== undefined
            ? `${weatherRes.value.current_weather.windspeed} km/h`
            : prev.weatherWind,
        quote:
          quoteRes.status === "fulfilled" && quoteRes.value?.quote
            ? quoteRes.value.quote
            : prev.quote,
        author:
          quoteRes.status === "fulfilled" && quoteRes.value?.author
            ? quoteRes.value.author
            : prev.author,
      }));
    } catch {
      setExternalData((prev) => ({ ...prev, loading: false }));
    }
  };

  const fetchSoapCountry = async (iso) => {
    setSelectedIso(iso);
    try {
      const data = await getSoapCountryApi(iso);
      setSoapCountry(data);
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    fetchThirdPartyApis();
    fetchSoapCountry("MX");
  }, []);

  return (
    <div className="dashboard-admin">
      <div className="dashboard-admin__header">
        <div>
          <h1>Dashboard Page — Tienda Online</h1>
          <h3>
            Bienvenido <strong>{user.email}</strong> (Usuario: {user.username} |
            Teléfono: {user.telefono || "6531234567"})
          </h3>
        </div>
        <Button
          negative
          icon
          labelPosition="left"
          onClick={logout}
        >
          <Icon name="sign-out" />
          Cerrar Sesión
        </Button>
      </div>

      <div className="dashboard-admin__grid">
        {/* Widget 1: API de Terceros con fetch (Unidad 3) */}
        <div className="dashboard-admin__card">
          <h2>
            <Icon name="globe" color="blue" />
            Widget API de Terceros (Open-Meteo, ExchangeRate & DummyJSON)
          </h2>
          <p style={{ color: "#475569", marginBottom: "14px" }}>
            Datos externos consumidos en tiempo real desde el Frontend usando{" "}
            <code>fetch()</code>:
          </p>
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "1fr 1fr",
              gap: "12px",
              marginBottom: "14px",
            }}
          >
            <div
              style={{
                background: "#eff6ff",
                padding: "14px",
                borderRadius: "12px",
                border: "1px solid #bfdbfe",
              }}
            >
              <div style={{ fontSize: "12px", color: "#1d4ed8", fontWeight: 700 }}>
                TIPO DE CAMBIO (API EXTERNA)
              </div>
              <div style={{ fontSize: "22px", fontWeight: 700, color: "#1e3a8a", marginTop: "4px" }}>
                1 USD = ${externalData.usdMxn} MXN
              </div>
              <div style={{ fontSize: "13px", color: "#3b82f6" }}>
                1 USD = €{externalData.usdEur} EUR
              </div>
            </div>

            <div
              style={{
                background: "#f0fdf4",
                padding: "14px",
                borderRadius: "12px",
                border: "1px solid #bbf7d0",
              }}
            >
              <div style={{ fontSize: "12px", color: "#15803d", fontWeight: 700 }}>
                CLIMA ACTUAL ({externalData.city})
              </div>
              <div style={{ fontSize: "22px", fontWeight: 700, color: "#14532d", marginTop: "4px" }}>
                {externalData.weatherTemp}
              </div>
              <div style={{ fontSize: "13px", color: "#16a34a" }}>
                Viento: {externalData.weatherWind}
              </div>
            </div>
          </div>

          <div
            style={{
              background: "#f8fafc",
              padding: "14px 16px",
              borderRadius: "10px",
              borderLeft: "4px solid #0098d3",
              marginBottom: "14px",
            }}
          >
            <div style={{ fontStyle: "italic", color: "#1e293b" }}>
              "{externalData.quote}"
            </div>
            <div style={{ fontSize: "12px", color: "#64748b", marginTop: "6px" }}>
              — {externalData.author} (API de terceros vía fetch)
            </div>
          </div>

          <Button
            size="small"
            primary
            icon
            labelPosition="left"
            onClick={fetchThirdPartyApis}
          >
            <Icon name="refresh" />
            Actualizar API de Terceros
          </Button>
        </div>

        {/* Widget 2: Web Service Propio (/auth/me/) + Servicio SOAP (zeep) */}
        <div className="dashboard-admin__card">
          <h2>
            <Icon name="server" color="teal" />
            Web Service SOAP (zeep) y Datos Protegidos JWT
          </h2>
          <p style={{ color: "#475569", marginBottom: "12px" }}>
            Respuesta del endpoint <code>/api/v1/soap/pais/?codigo={selectedIso}</code>{" "}
            consumiendo el WSDL público <code>CountryInfoService.wso?WSDL</code> con{" "}
            <strong>zeep</strong>:
          </p>

          <div style={{ marginBottom: "14px" }}>
            <Button.Group size="small">
              <Button
                active={selectedIso === "MX"}
                color={selectedIso === "MX" ? "teal" : undefined}
                onClick={() => fetchSoapCountry("MX")}
              >
                México (MX)
              </Button>
              <Button
                active={selectedIso === "US"}
                color={selectedIso === "US" ? "teal" : undefined}
                onClick={() => fetchSoapCountry("US")}
              >
                Estados Unidos (US)
              </Button>
              <Button
                active={selectedIso === "ES"}
                color={selectedIso === "ES" ? "teal" : undefined}
                onClick={() => fetchSoapCountry("ES")}
              >
                España (ES)
              </Button>
            </Button.Group>
          </div>

          {soapCountry && (
            <div
              style={{
                background: "#f8fafc",
                padding: "14px 16px",
                borderRadius: "12px",
                border: "1px solid #cbd5e1",
                fontSize: "14px",
                lineHeight: "1.7",
              }}
            >
              <div>
                <strong>Protocolo:</strong>{" "}
                <Label color="teal" size="tiny">
                  {soapCountry.protocolo}
                </Label>
              </div>
              <div>
                <strong>País:</strong> {soapCountry.pais} ({soapCountry.codigo_iso})
              </div>
              <div>
                <strong>Capital:</strong> {soapCountry.capital} |{" "}
                <strong>Moneda ISO:</strong> {soapCountry.moneda_iso} |{" "}
                <strong>Prefijo telefónico:</strong> {soapCountry.codigo_telefono}
              </div>
              <div>
                <strong>Idiomas:</strong>{" "}
                {(soapCountry.idiomas || []).join(", ")}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
