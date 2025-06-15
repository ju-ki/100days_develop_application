import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <form method="GET" action="http://127.0.0.1:5000/api/url">
          <label>
            url入力欄
          </label>
            <input type="text" name="url" placeholder="Enter url" required />
            <button type="submit">Submit</button>
        </form>
      </header>
    </div>
  );
}

export default App;
