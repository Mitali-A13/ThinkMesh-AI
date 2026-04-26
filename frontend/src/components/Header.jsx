import { useNavigate } from "react-router-dom";

export default function Header({ user, onLogout }) {
  const navigate = useNavigate();
  return (
    <div style={styles.header}>
      <div>
        <h3>Dashboard</h3>
      </div>

      <div>
        <span>{user?.name}</span>

        <button
          onClick={onLogout}
          style={styles.button}
        >
          Logout
        </button>

        <button onClick={() => navigate("/settings")}>
          Settings
        </button>
      </div>
    </div>
  );
}

const styles = {
  header: {
    display: "flex",
    justifyContent: "space-between",
    marginBottom: "30px",
  },
  button: {
    marginLeft: "15px",
  },
};