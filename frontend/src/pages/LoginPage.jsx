import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import api from "../services/api";
import { saveToken } from "../services/auth";

export default function LoginPage() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    email: "",
    password: "",
  });

  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      setLoading(true);

      const res = await api.post(
        "/login",
        form
      );

      saveToken(res.data.access_token);

      navigate("/dashboard");
    } catch (error) {
      alert(
        error.response?.data?.detail ||
        "Login failed"
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1>Login</h1>

      <form onSubmit={handleSubmit}>
        <input
          name="email"
          placeholder="Email"
          onChange={handleChange}
        />

        <input
          type="password"
          name="password"
          placeholder="Password"
          onChange={handleChange}
        />

        <button type="submit">
          {loading ? "Loading..." : "Login"}
        </button>
      </form>

      <Link to="/signup">
        Create account
      </Link>
    </div>
  );
}