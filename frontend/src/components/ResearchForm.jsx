import { useState } from "react";

export default function ResearchForm({
  onSubmit,
  loading,
}) {
  const [topic, setTopic] = useState("");

  function handleSubmit(e) {
    e.preventDefault();

    if (!topic.trim()) return;

    onSubmit(topic);
  }

  return (
    <form onSubmit={handleSubmit}>
      <textarea
        rows="5"
        placeholder="Enter research topic..."
        value={topic}
        onChange={(e) =>
          setTopic(e.target.value)
        }
        style={styles.textarea}
      />

      <button
        type="submit"
        disabled={loading}
      >
        {loading
          ? "Generating..."
          : "Generate Report"}
      </button>
    </form>
  );
}

const styles = {
  textarea: {
    width: "100%",
    padding: "12px",
    marginBottom: "12px",
  },
};