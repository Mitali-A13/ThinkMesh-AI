export default function HistorySidebar({
  history,
  onOpen,
  onDelete,
}) {
  return (
    <div style={styles.sidebar}>
      <h2>ThinkMesh AI</h2>
      <p>History</p>

      {history.map((item) => (
        <div key={item.id} style={styles.card}>
          <div
            onClick={() => onOpen(item.id)}
            style={{
              cursor: "pointer",
              marginBottom: "8px",
            }}
          >
            <strong>{item.topic}</strong>
            <p>{item.created_at}</p>
          </div>

          <button
            onClick={() => onDelete(item.id)}
          >
            Delete
          </button>
        </div>
      ))}
    </div>
  );
}

const styles = {
  sidebar: {
    width: "280px",
    minHeight: "100vh",
    padding: "20px",
    background: "#111827",
    color: "white",
    overflowY: "auto",
  },
  card: {
    marginTop: "15px",
    padding: "10px",
    border: "1px solid #333",
    borderRadius: "10px",
  },
};