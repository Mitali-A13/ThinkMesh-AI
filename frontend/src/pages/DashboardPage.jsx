import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import api from "../services/api";
import { removeToken } from "../services/auth";

import HistorySidebar from "../components/HistorySidebar";
import Header from "../components/Header";
import ResearchForm from "../components/ResearchForm";
import Loader from "../components/Loader";
import ReportCard from "../components/ReportCard";

export default function DashboardPage() {
  const navigate = useNavigate();

  const [user, setUser] = useState(null);
  const [loadingUser, setLoadingUser] =
    useState(true);

  const [loadingReport, setLoadingReport] =
    useState(false);

  const [report, setReport] = useState("");
  const [feedback, setFeedback] = useState("");
  const [error, setError] = useState("");

  const [history, setHistory] = useState([]);

  useEffect(() => {
    fetchUser();
    fetchHistory();
  }, []);

  async function fetchUser() {
    try {
      const res = await api.get("/me");
      setUser(res.data.user);
    } catch (error) {
      removeToken();
      navigate("/");
    } finally {
      setLoadingUser(false);
    }
  }

  async function handleResearch(topic) {
  try {
    setLoadingReport(true);
    setError("");
    setReport("");
    setFeedback("");

    const res = await api.post("/research", {
      topic,
    });

    setReport(res.data.data.report);
    setFeedback(res.data.data.feedback);

    fetchHistory();

  } catch (error) {
    setError("Failed to generate report");
  } finally {
    setLoadingReport(false);
  }
}

  function logout() {
    removeToken();
    navigate("/");
  }

  async function fetchHistory() {
    try {
      const res = await api.get("/history");
      setHistory(res.data.history);
    } catch (error) {
      console.error(error);
    }
  }

  async function openHistory(id) {
    try {
      const res = await api.get(`/history/${id}`);

      setReport(res.data.history.report);
      setFeedback(res.data.history.feedback);

    } catch (error) {
      console.error(error);
      setError("Failed to open history");
    }
  }

  async function deleteHistory(id) {
    try {
      await api.delete(`/history/${id}`);

      fetchHistory();

    } catch (error) {
      console.error(error);
    }
  }


  if (loadingUser) return <p>Loading...</p>;

  return (
  <div style={styles.layout}>
    <HistorySidebar
      history={history}
      onOpen={openHistory}
      onDelete={deleteHistory}
    />

    <div style={styles.main}>
      <Header
        user={user}
        onLogout={logout}
      />

      <ResearchForm
        onSubmit={handleResearch}
        loading={loadingReport}
      />

      {loadingReport && <Loader />}

      {error && (
        <p style={{ color: "red", marginTop: "20px" }}>
          {error}
        </p>
      )}

      {report && (
        <ReportCard
          title="Research Report"
          content={report}
        />
      )}

      {feedback && (
        <ReportCard
          title="Critic Feedback"
          content={feedback}
        />
      )}
    </div>
  </div>
  );
}

const styles = {
  layout: {
    display: "flex",
    minHeight: "100vh",
    background: "#0b0d10",
    color: "white",
  },

  main: {
    flex: 1,
    padding: "30px",
    overflowY: "auto",
  },
};