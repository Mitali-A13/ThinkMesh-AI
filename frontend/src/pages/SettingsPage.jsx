import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import api from "../services/api";
import { removeToken } from "../services/auth";

export default function SettingsPage() {
  const navigate = useNavigate();

  const [user, setUser] = useState(null);

  const [oldPassword, setOldPassword] =
    useState("");

  const [newPassword, setNewPassword] =
    useState("");

  const [message, setMessage] =
    useState("");

  const [error, setError] =
    useState("");

  useEffect(() => {
    fetchUser();
  }, []);

  async function fetchUser() {
    try {
      const res = await api.get("/me");
      setUser(res.data.user);
    } catch {
      navigate("/");
    }
  }

  async function handleChangePassword(e) {
    e.preventDefault();

    try {
      setMessage("");
      setError("");

      await api.put("/change-password", {
        current_password: oldPassword,
        new_password: newPassword,
      });

      setMessage(
        "Password changed successfully"
      );

      setOldPassword("");
      setNewPassword("");

    } catch (error) {
      setError(
        error.response?.data?.detail ||
        "Failed to change password"
      );
    }
  }

  function logout() {
    removeToken();
    navigate("/");
  }

  return (
    <div style={styles.page}>
      <h1>Settings</h1>

      {user && (
        <div style={styles.card}>
          <h2>Profile</h2>
          <p>Name: {user.name}</p>
          <p>Email: {user.email}</p>
        </div>
      )}

      <form
        onSubmit={handleChangePassword}
        style={styles.card}
      >
        <h2>Change Password</h2>

        <input
          type="password"
          placeholder="Old Password"
          value={oldPassword}
          onChange={(e) =>
            setOldPassword(e.target.value)
          }
          required
        />

        <input
          type="password"
          placeholder="New Password"
          value={newPassword}
          onChange={(e) =>
            setNewPassword(e.target.value)
          }
          required
        />

        <button type="submit">
          Update Password
        </button>

        {message && (
          <p style={{ color: "green" }}>
            {message}
          </p>
        )}

        {error && (
          <p style={{ color: "red" }}>
            {error}
          </p>
        )}
      </form>

      <button
        onClick={logout}
        style={styles.logout}
      >
        Logout
      </button>
    </div>
  );
}

const styles = {
  page: {
    minHeight: "100vh",
    background: "#0b0d10",
    color: "white",
    padding: "30px",
  },

  card: {
    background: "#111827",
    padding: "20px",
    borderRadius: "10px",
    marginBottom: "20px",
    display: "flex",
    flexDirection: "column",
    gap: "10px",
    maxWidth: "500px",
  },

  logout: {
    padding: "10px 16px",
    cursor: "pointer",
  },
};