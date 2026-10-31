"use client";

import { useCallback, useEffect, useState, type FormEvent } from "react";
import type { Session } from "@supabase/supabase-js";
import { getSupabase } from "../lib/supabase";

type Profile = { id: string; nombre: string; correo_verificado: boolean };
type Publication = {
  id: string; titulo: string; region: string; comuna: string; precio_clp: number;
  cupos_totales: number; tipo: string; estado: string; fecha_publicacion: string;
};

const API = (process.env.NEXT_PUBLIC_API_BASE_URL || "").replace(/\/$/, "");

async function requestApi<T>(path: string, accessToken?: string, options?: RequestInit): Promise<T> {
  if (!API) throw new Error("Falta NEXT_PUBLIC_API_BASE_URL en Vercel/web/.env.local");
  const headers: Record<string, string> = { "Content-Type": "application/json" };
  if (accessToken) headers.Authorization = `Bearer ${accessToken}`;
  const response = await fetch(`${API}${path}`, {
    ...options,
    headers: { ...headers, ...(options?.headers || {}) },
    cache: "no-store",
  });
  const text = await response.text();
  let body: unknown;
  try { body = text ? JSON.parse(text) : null; } catch { body = text; }
  if (!response.ok) {
    const err = typeof body === "object" && body !== null && "detail" in body
      ? String((body as { detail: unknown }).detail)
      : String(body ?? "Error de servidor");
    throw new Error(`${response.status}: ${err}`);
  }
  return body as T;
}

export default function Home() {
  const [session, setSession] = useState<Session | null>(null);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [otp, setOtp] = useState("");
  const [nombre, setNombre] = useState("");
  const [titulo, setTitulo] = useState("Habitación cerca de la UCT");
  const [region, setRegion] = useState("La Araucanía");
  const [comuna, setComuna] = useState("Temuco");
  const [precio, setPrecio] = useState("180000");
  const [cupos, setCupos] = useState("2");
  const [profile, setProfile] = useState<Profile | null>(null);
  const [publicaciones, setPublicaciones] = useState<Publication[]>([]);
  const [message, setMessage] = useState("Prueba de concepto: datos separados por servicio, persistencia real.");
  const [busy, setBusy] = useState(false);
  const supabase = getSupabase();

  const refreshListings = useCallback(async () => {
    try { setPublicaciones(await requestApi<Publication[]>("/publicaciones")); }
    catch (error) { setMessage(`Listado: ${String(error)}`); }
  }, []);

  const refreshProfile = useCallback(async (token: string) => {
    try {
      const p = await requestApi<Profile>("/usuarios/me", token);
      setProfile(p);
      setNombre(p.nombre);
    } catch (error) {
      setProfile(null);
      setMessage(`Perfil: ${String(error)}. Puedes crearlo desde este formulario.`);
    }
  }, []);

  useEffect(() => {
    if (!supabase) return;
    supabase.auth.getSession().then(({ data }) => setSession(data.session));
    const { data: sub } = supabase.auth.onAuthStateChange((_event, updated) => setSession(updated));
    return () => sub.subscription.unsubscribe();
  }, [supabase]);

  useEffect(() => { void refreshListings(); }, [refreshListings]);
  useEffect(() => { if (session?.access_token) void refreshProfile(session.access_token); else setProfile(null); }, [session?.access_token, refreshProfile]);

  async function act(fn: () => Promise<void>) {
    setBusy(true);
    try { await fn(); } catch (error) { setMessage(String(error)); }
    finally { setBusy(false); }
  }

  function onLogin(event: FormEvent) {
    event.preventDefault();
    void act(async () => {
      if (!supabase) throw Error("Configura NEXT_PUBLIC_SUPABASE_URL y NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY");
      const { error } = await supabase.auth.signInWithPassword({ email, password });
      if (error) throw error;
      setMessage("Sesión Supabase Auth iniciada.");
    });
  }

  function onRegister() {
    void act(async () => {
      if (!supabase) throw Error("Supabase no está configurado");
      const { error } = await supabase.auth.signUp({ email, password });
      if (error) throw error;
      setMessage("Registro enviado. Revisa tu correo y verifica la cuenta antes de publicar.");
    });
  }

  function onVerifyOtp() {
    void act(async () => {
      if (!supabase) throw Error("Supabase no configurado");
      const { error } = await supabase.auth.verifyOtp({ email, token: otp, type: "signup" });
      if (error) throw error;
      setMessage("Correo verificado por Supabase Auth. Ya puedes completar tu perfil.");
    });
  }

  function onSaveProfile(event: FormEvent) {
    event.preventDefault();
    void act(async () => {
      if (!session) throw Error("Primero inicia sesión");
      const result = await requestApi<Profile>("/usuarios/me", session.access_token, {
        method: "PUT", body: JSON.stringify({ nombre }),
      });
      setProfile(result);
      setMessage("Perfil guardado en auth_users.profiles; no en Listado.");
    });
  }

  function onCreate(event: FormEvent) {
    event.preventDefault();
    void act(async () => {
      if (!session) throw Error("Primero inicia sesión");
      const result = await requestApi<Publication>("/publicaciones/compartidas", session.access_token, {
        method: "POST",
        body: JSON.stringify({
          titulo, region, comuna, precio_clp: Number(precio), cupos_totales: Number(cupos),
        }),
      });
      setMessage(`Publicación ${result.id} persistida. Listado consultó a Auth/Users mediante HTTP.`);
      await refreshListings();
    });
  }

  return (
    <main className="site">
      <header className="topbar">
        <div className="brand"><span className="brand-icon">R</span><span>roomies<span className="dot">.</span></span></div>
        <span className="environment">LABORATORIO · NO PRODUCCIÓN</span>
      </header>

      <section className="intro">
        <div className="eyebrow">Taller de Integración IV · PoC arquitectónica</div>
        <h1>De una interfaz a <em>tres plataformas</em>.</h1>
        <p>Una aplicación mínima de Roomies para probar Vercel, FastAPI en Render y Supabase de extremo a extremo.</p>
        <div className="chips"><span>▲ Vercel · Next.js</span><span>⬡ Render · Gateway + 2 APIs</span><span>▣ Supabase · Auth + PostgreSQL</span></div>
      </section>

      <div className="alert" role="status">{message}</div>

      <div className="layout">
        <section className="panel">
          <div className="panel-head"><span className="index">01</span><h2>Identidad</h2><span className="tag">Supabase Auth</span></div>
          {session ? (
            <div>
              <p>Sesión iniciada como <strong>{session.user.email}</strong></p>
              <p className="tiny">UUID: {session.user.id}</p>
              <p className="tiny">Correo confirmado: {session.user.email_confirmed_at ? "Sí" : "No"}</p>
              <button disabled={busy} className="secondary" onClick={() => void act(async () => { await supabase?.auth.signOut(); setMessage("Sesión finalizada"); })}>Cerrar sesión</button>
            </div>
          ) : (
            <form onSubmit={onLogin}>
              <label>Correo electrónico<input required value={email} type="email" onChange={e => setEmail(e.target.value)} placeholder="correo@ejemplo.cl" /></label>
              <label>Contraseña<input required value={password} type="password" minLength={6} onChange={e => setPassword(e.target.value)} placeholder="••••••••" /></label>
              <div className="btn-row"><button disabled={busy} type="submit">Ingresar</button><button disabled={busy} type="button" className="secondary" onClick={onRegister}>Registrarse</button></div>
              <div className="otp"><label>¿Recibiste un código de verificación?<input value={otp} onChange={e => setOtp(e.target.value)} inputMode="numeric" placeholder="Código recibido por correo" /></label><button disabled={busy || !otp} type="button" className="secondary" onClick={onVerifyOtp}>Verificar correo</button></div>
            </form>
          )}
        </section>

        <section className="panel">
          <div className="panel-head"><span className="index">02</span><h2>Mi perfil</h2><span className="tag">Auth/Users</span></div>
          <form onSubmit={onSaveProfile}>
            <label>Nombre visible<input value={nombre} onChange={e => setNombre(e.target.value)} minLength={2} required placeholder="Tu nombre" /></label>
            <div className="statusline"><span className={profile ? "status good" : "status"}></span>{profile ? "Perfil encontrado en PostgreSQL" : "Sin perfil cargado"}</div>
            <button disabled={busy || !session} type="submit">Guardar perfil</button>
          </form>
        </section>

        <section className="panel span-two">
          <div className="panel-head"><span className="index">03</span><h2>Crear publicación compartida</h2><span className="tag">Listado → Auth/Users</span></div>
          <form onSubmit={onCreate}>
            <div className="fields"><label className="wide">Título<input value={titulo} onChange={e => setTitulo(e.target.value)} minLength={5} required /></label><label>Región<input value={region} onChange={e => setRegion(e.target.value)} required /></label><label>Comuna<input value={comuna} onChange={e => setComuna(e.target.value)} required /></label><label>Precio mensual (CLP)<input value={precio} onChange={e => setPrecio(e.target.value)} min={1} type="number" required /></label><label>Cupos totales<input value={cupos} onChange={e => setCupos(e.target.value)} min={1} max={20} type="number" required /></label></div>
            <button disabled={busy || !session || !profile?.correo_verificado} type="submit">Publicar en Roomies PoC</button>
          </form>
          <p className="tiny">El backend valida JWT y correo verificado; el servicio Listado comprueba el autor llamando al servicio Auth/Users por HTTP.</p>
        </section>

        <section className="panel span-two">
          <div className="panel-head"><span className="index">04</span><h2>Publicaciones persistidas</h2><span className="tag">API pública de lectura</span></div>
          <div className="btn-row"><button className="secondary" onClick={() => void refreshListings()} disabled={busy}>Actualizar listado</button></div>
          <div className="listings">
            {publicaciones.length ? publicaciones.map(p => (
              <article key={p.id} className="listing"><div className="listing-icon">⌂</div><div><h3>{p.titulo}</h3><p>{p.comuna}, {p.region} · {p.cupos_totales} cupo(s)</p></div><strong>{p.precio_clp.toLocaleString("es-CL", { style: "currency", currency: "CLP", maximumFractionDigits: 0 })}</strong></article>
            )) : <p>No hay publicaciones o el Gateway todavía no responde.</p>}
          </div>
        </section>
      </div>
      <footer>PoC educativa · Los datos, identidades y claves son de un proyecto Supabase de prueba. No incorporar documentos personales reales.</footer>
    </main>
  );
}
