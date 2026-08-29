import { useState } from 'react';
import { SignedIn, SignedOut, SignInButton, UserButton, useAuth } from "@clerk/clerk-react";
import './App.css';

const API_BASE = "http://127.0.0.1:8000";

function App() {
  const { getToken } = useAuth();
  
  // State for Add Credits
  const [creditEmail, setCreditEmail] = useState("");
  const [creditAmount, setCreditAmount] = useState("");
  const [creditStatus, setCreditStatus] = useState({ message: "", type: "" });
  const [creditLoading, setCreditLoading] = useState(false);

  // State for Block User
  const [blockEmail, setBlockEmail] = useState("");
  const [blockStatus, setBlockStatus] = useState({ message: "", type: "" });
  const [blockLoading, setBlockLoading] = useState(false);

  // State for Unblock User
  const [unblockEmail, setUnblockEmail] = useState("");
  const [unblockStatus, setUnblockStatus] = useState({ message: "", type: "" });
  const [unblockLoading, setUnblockLoading] = useState(false);

  const handleAddCredits = async (e) => {
    e.preventDefault();
    if (!creditEmail || !creditAmount) return;
    setCreditStatus({ message: "", type: "" });
    setCreditLoading(true);

    try {
      const token = await getToken();
      const res = await fetch(`${API_BASE}/admin/add-credits`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({ email: creditEmail, balance: parseFloat(creditAmount) })
      });
      const data = await res.json();
      if (res.ok) {
        setCreditStatus({ message: `Successfully added $${creditAmount} to ${creditEmail}`, type: "success" });
        setCreditEmail("");
        setCreditAmount("");
      } else {
        setCreditStatus({ message: data.detail || "Error adding credits", type: "error" });
      }
    } catch (error) {
      setCreditStatus({ message: "Network error", type: "error" });
    } finally {
      setCreditLoading(false);
    }
  };

  const handleBlockUser = async (e) => {
    e.preventDefault();
    if (!blockEmail) return;
    setBlockStatus({ message: "", type: "" });
    setBlockLoading(true);

    try {
      const token = await getToken();
      const res = await fetch(`${API_BASE}/admin/block-user`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({ email: blockEmail })
      });
      const data = await res.json();
      if (res.ok) {
        setBlockStatus({ message: `${blockEmail} has been blocked`, type: "success" });
        setBlockEmail("");
      } else {
        setBlockStatus({ message: data.detail || "Error blocking user", type: "error" });
      }
    } catch (error) {
      setBlockStatus({ message: "Network error", type: "error" });
    } finally {
      setBlockLoading(false);
    }
  };

  const handleUnblockUser = async (e) => {
    e.preventDefault();
    if (!unblockEmail) return;
    setUnblockStatus({ message: "", type: "" });
    setUnblockLoading(true);

    try {
      const token = await getToken();
      const res = await fetch(`${API_BASE}/admin/unblock-user`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({ email: unblockEmail })
      });
      const data = await res.json();
      if (res.ok) {
        setUnblockStatus({ message: `${unblockEmail} has been unblocked`, type: "success" });
        setUnblockEmail("");
      } else {
        setUnblockStatus({ message: data.detail || "Error unblocking user", type: "error" });
      }
    } catch (error) {
      setUnblockStatus({ message: "Network error", type: "error" });
    } finally {
      setUnblockLoading(false);
    }
  };

  return (
    <div className="app-container">
      <header className="header">
        <div>
          <h1>Control Panel</h1>
        </div>
        <SignedIn>
          <div className="user-profile">
            <span className="badge-admin">ADMIN</span>
            <UserButton afterSignOutUrl="/" />
          </div>
        </SignedIn>
      </header>

      <SignedOut>
        <div className="auth-container">
          <h2>Admin Authentication Required</h2>
          <p>Please sign in with an administrator account to access the control panel.</p>
          <SignInButton mode="modal">
            <button className="btn btn-primary" style={{ maxWidth: "200px" }}>
              Sign In
            </button>
          </SignInButton>
        </div>
      </SignedOut>

      <SignedIn>
        <main className="dashboard-grid">
          
          {/* Add Credits Card */}
          <section className="card card-full">
            <h2 className="card-title">Add Credits</h2>
            <form onSubmit={handleAddCredits}>
              <div className="dashboard-grid">
                <div className="form-group">
                  <label>User Email</label>
                  <input 
                    type="email" 
                    className="form-control" 
                    placeholder="user@example.com"
                    value={creditEmail}
                    onChange={(e) => setCreditEmail(e.target.value)}
                    required
                  />
                </div>
                <div className="form-group">
                  <label>Amount ($)</label>
                  <input 
                    type="number" 
                    className="form-control" 
                    placeholder="0.00"
                    min="0.01"
                    step="0.01"
                    value={creditAmount}
                    onChange={(e) => setCreditAmount(e.target.value)}
                    required
                  />
                </div>
              </div>
              <button type="submit" className="btn btn-success" disabled={creditLoading}>
                {creditLoading ? "Adding..." : "Deposit Funds"}
              </button>
              {creditStatus.message && (
                <div className={`status-message status-${creditStatus.type}`}>
                  {creditStatus.message}
                </div>
              )}
            </form>
          </section>

          {/* Block User Card */}
          <section className="card">
            <h2 className="card-title">Block User</h2>
            <form onSubmit={handleBlockUser}>
              <div className="form-group">
                <label>User Email</label>
                <input 
                  type="email" 
                  className="form-control" 
                  placeholder="user@example.com"
                  value={blockEmail}
                  onChange={(e) => setBlockEmail(e.target.value)}
                  required
                />
              </div>
              <button type="submit" className="btn btn-danger" disabled={blockLoading}>
                {blockLoading ? "Processing..." : "Block Account"}
              </button>
              {blockStatus.message && (
                <div className={`status-message status-${blockStatus.type}`}>
                  {blockStatus.message}
                </div>
              )}
            </form>
          </section>

          {/* Unblock User Card */}
          <section className="card">
            <h2 className="card-title">Unblock User</h2>
            <form onSubmit={handleUnblockUser}>
              <div className="form-group">
                <label>User Email</label>
                <input 
                  type="email" 
                  className="form-control" 
                  placeholder="user@example.com"
                  value={unblockEmail}
                  onChange={(e) => setUnblockEmail(e.target.value)}
                  required
                />
              </div>
              <button type="submit" className="btn btn-primary" disabled={unblockLoading}>
                {unblockLoading ? "Processing..." : "Restore Account"}
              </button>
              {unblockStatus.message && (
                <div className={`status-message status-${unblockStatus.type}`}>
                  {unblockStatus.message}
                </div>
              )}
            </form>
          </section>

        </main>
      </SignedIn>
    </div>
  );
}

export default App;
