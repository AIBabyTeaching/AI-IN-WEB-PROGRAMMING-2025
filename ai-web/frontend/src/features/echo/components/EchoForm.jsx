// Presentational component responsible for rendering the echo form and results.
//
// The component receives all state and handlers from the `useEchoForm` hook so it
// can focus on markup and teaching-friendly comments.
import PropTypes from 'prop-types';

export function EchoForm({
  msg,
  setMsg,
  handleSubmit,
  loading,
  error,
  response,
}) {
  return (
    <section style={{ display: 'grid', gap: 16, maxWidth: 420 }}>
      <header>
        <h1>Lab 2 — Echo with retries</h1>
        <p>
          This form mirrors the curriculum&apos;s feature-folder layout. Submit a message to see
          how the frontend retries the flaky endpoint before succeeding.
        </p>
      </header>
      <form onSubmit={handleSubmit} style={{ display: 'grid', gap: 12 }}>
        <label htmlFor="msg">Message to echo</label>
        <input
          id="msg"
          value={msg}
          onChange={(event) => setMsg(event.target.value)}
          disabled={loading}
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Sending…' : 'Send'}
        </button>
      </form>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {response && (
        <article>
          <h2>Server response</h2>
          <pre>{response}</pre>
        </article>
      )}
    </section>
  );
}

EchoForm.propTypes = {
  msg: PropTypes.string.isRequired,
  setMsg: PropTypes.func.isRequired,
  handleSubmit: PropTypes.func.isRequired,
  loading: PropTypes.bool.isRequired,
  error: PropTypes.string.isRequired,
  response: PropTypes.string.isRequired,
};
