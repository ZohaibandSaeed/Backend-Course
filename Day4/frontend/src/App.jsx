import { useState, useEffect } from 'react';
import { SignedIn, SignedOut, SignInButton, UserButton, useUser, useAuth } from "@clerk/clerk-react";
import './App.css';

const API_BASE = "http://127.0.0.1:8000";

function App() {
  const { user } = useUser();
  const { getToken } = useAuth();
  
  const [balance, setBalance] = useState(0.0);
  const [myId, setMyId] = useState(null);
  const [transactions, setTransactions] = useState([]);
  
  const [receiverEmail, setReceiverEmail] = useState("");
  const [amount, setAmount] = useState("");
  const [loading, setLoading] = useState(false);
  
  const [status, setStatus] = useState({ message: "", type: "" });

  // Sync user to DB when logged in
  useEffect(() => {
    const syncAndFetchData = async () => {
      if (!user) return;
      
      try {
        // 1. Sync User
        await fetch(`${API_BASE}/sync-user`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            clerk_user_id: user.id,
            name: user.fullName || user.firstName || "Unknown User",
            email: user.primaryEmailAddress?.emailAddress
          })
        });

        // 2. Fetch Dashboard Data (Balance and History)
        await fetchDashboardData();
        
      } catch (error) {
        console.error("Initialization Error:", error);
      }
    };

    syncAndFetchData();
  }, [user]);

  const fetchDashboardData = async () => {
    try {
      const token = await getToken();
      if (!token) return;

      const headers = {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
      };

      // Fetch Profile (Balance)
      const profileRes = await fetch(`${API_BASE}/me`, { headers });
      if (profileRes.ok) {
        const profileData = await profileRes.json();
        setBalance(profileData.user_data.balance);
        setMyId(profileData.user_data.id);
      }

      // Fetch History
      const historyRes = await fetch(`${API_BASE}/user/transaction-history`, { headers });
      if (historyRes.ok) {
        const historyData = await historyRes.json();
        setTransactions(historyData.history);
      }
    } catch (error) {
      console.error("Error fetching dashboard data:", error);
    }
  };

  const handleTransfer = async (e) => {
    e.preventDefault();
    if (!receiverEmail || !amount) return;
    
    setStatus({ message: "", type: "" });
    setLoading(true);

    try {
      const token = await getToken();
      const res = await fetch(`${API_BASE}/user/transfer`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({
          receiver_email: receiverEmail,
          amount: parseFloat(amount)
        })
      });

      const data = await res.json();

      if (res.ok) {
        setStatus({ message: "Money transferred successfully! 🎉", type: "success" });
        setReceiverEmail("");
        setAmount("");
        // Refresh data
        await fetchDashboardData();
      } else {
        setStatus({ message: data.detail || "Transfer failed.", type: "error" });
      }
    } catch (error) {
      setStatus({ message: "Network error occurred.", type: "error" });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <header className="header">
        <h1>SendCash</h1>
        <SignedIn>
          <div className="user-profile">
            <span className="welcome-text">Hi, {user?.firstName}</span>
            <UserButton afterSignOutUrl="/" />
          </div>
        </SignedIn>
      </header>

      <SignedOut>
        <div className="auth-container">
          <p>Securely transfer money to anyone.</p>
          <SignInButton mode="modal">
            <button className="btn btn-primary" style={{ maxWidth: "200px" }}>
              Sign In to Continue
            </button>
          </SignInButton>
        </div>
      </SignedOut>

      <SignedIn>
        <main>
          {/* Balance Card */}
          <section className="card balance-card">
            <div className="balance-label">Available Balance</div>
            <div className="balance-amount">${balance.toFixed(2)}</div>
          </section>

          {/* Transfer Form Card */}
          <section className="card">
            <h2 className="section-title">Send Money</h2>
            <form onSubmit={handleTransfer}>
              <div className="form-group">
                <label>Receiver Email</label>
                <input 
                  type="email" 
                  className="form-control" 
                  placeholder="e.g. ali@example.com"
                  value={receiverEmail}
                  onChange={(e) => setReceiverEmail(e.target.value)}
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
                  value={amount}
                  onChange={(e) => setAmount(e.target.value)}
                  required
                />
              </div>
              
              <button type="submit" className="btn btn-primary" disabled={loading}>
                {loading ? "Sending..." : "Send Money"}
              </button>

              {status.message && (
                <div className={`status-message status-${status.type}`}>
                  {status.message}
                </div>
              )}
            </form>
          </section>

          {/* Transaction History Card */}
          <section className="card">
            <h2 className="section-title">Recent Transactions</h2>
            
            {transactions.length === 0 ? (
              <p style={{ color: "var(--text-muted)", textAlign: "center" }}>No transactions yet.</p>
            ) : (
              <div className="transaction-list">
                {transactions.map((tx) => {
                  const isSender = tx.sender_id === myId;
                  
                  return (
                    <div className="transaction-item" key={tx.id}>
                      <div className="transaction-info">
                        <span className="transaction-type">
                          {isSender ? "Sent Money" : "Received Money"}
                        </span>
                        <span className="transaction-date">
                          {new Date(tx.created_at).toLocaleDateString()}
                        </span>
                      </div>
                      <div className={`transaction-amount ${isSender ? "amount-out" : "amount-in"}`}>
                        {isSender ? "-" : "+"} ${tx.amount.toFixed(2)}
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </section>
        </main>
      </SignedIn>
    </div>
  );
}

export default App;
