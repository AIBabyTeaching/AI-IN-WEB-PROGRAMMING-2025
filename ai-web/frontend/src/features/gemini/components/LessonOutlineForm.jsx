// Presentational component that renders the Gemini lesson outline form.
import PropTypes from 'prop-types';

export function LessonOutlineForm({ topic, setTopic, outline, loading, error, handleSubmit }) {
  return (
    <form onSubmit={handleSubmit} style={{ display: 'grid', gap: 12 }}>
      <p>
        Generate a quick lesson outline powered by Gemini. Provide a topic, submit
        the form, and discuss the generated talking points with your class.
      </p>

      <label style={{ display: 'grid', gap: 4 }}>
        <span>Lesson topic</span>
        <input
          type="text"
          value={topic}
          onChange={(event) => setTopic(event.target.value)}
          placeholder="e.g. Building resilient web APIs"
          disabled={loading}
          required
        />
      </label>

      <button type="submit" disabled={loading || !topic.trim()}>
        {loading ? 'Generating outline…' : 'Generate outline'}
      </button>

      {error && (
        <p style={{ color: 'crimson' }}>
          {error}. Confirm the backend has access to <code>GEMINI_API_KEY</code>.
        </p>
      )}

      {outline.length > 0 && (
        <ol>
          {outline.map((item, index) => (
            <li key={`${item}-${index}`}>{item}</li>
          ))}
        </ol>
      )}
    </form>
  );
}

LessonOutlineForm.propTypes = {
  topic: PropTypes.string.isRequired,
  setTopic: PropTypes.func.isRequired,
  outline: PropTypes.arrayOf(PropTypes.string).isRequired,
  loading: PropTypes.bool.isRequired,
  error: PropTypes.string,
  handleSubmit: PropTypes.func.isRequired
};

LessonOutlineForm.defaultProps = {
  error: null
};
