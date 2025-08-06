import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [date, setDate] = useState('');
  const [mood, setMood] = useState('');
  const [content, setContent] = useState('');
  const [image, setImage] = useState(null);
  const [imageUrl, setImageUrl] = useState('');

  const uploadImage = async () => {
    const formData = new FormData();
    formData.append('file', image);
    const res = await axios.post('http://localhost:5000/upload', formData);
    setImageUrl(res.data.url);
  };

  const submitEntry = async () => {
    if (image) await uploadImage();
    await axios.post('http://localhost:5000/journal', {
      date, mood, content, image_url: imageUrl
    });
    alert('Saved!');
  };

  return (
    <div className="container">
      <h1>My Journal</h1>
      <input type="date" value={date} onChange={e => setDate(e.target.value)} />
      <input type="text" placeholder="Mood" value={mood} onChange={e => setMood(e.target.value)} />
      <textarea placeholder="Write here..." value={content} onChange={e => setContent(e.target.value)} />
      <input type="file" onChange={e => setImage(e.target.files[0])} />
      <button onClick={submitEntry}>Save</button>
    </div>
  );
}

export default App;

