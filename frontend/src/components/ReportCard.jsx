export default function ReportCard({
  title,
  content,
}) {
  return (
    <div style={styles.card}>
      <h2>{title}</h2>

      <button
        onClick={() =>
            navigator.clipboard.writeText(content)
        }
        >
        Copy
      </button>

      <pre style={styles.text}>
        {content}
      </pre>
    </div>
  );
}

const styles = {
  card: {
    marginTop: "25px",
    padding: "20px",
    border: "1px solid #333",
    borderRadius: "12px",
    background: "#111827",
    color: "white",
  },
  text: {
    whiteSpace: "pre-wrap",
    lineHeight: "1.6",
    fontFamily: "inherit",
  },
};