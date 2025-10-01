<h1 align="center">Space Fabric Simulation</h1>

<p align="center">
  <img src="output.gif" width="700"/>
</p>

<p>
  This project is a Python-based simulation that models a simple <b>space fabric</b> and a <b>sun</b>. 
  Due to the sun’s mass, the fabric gets curved, visually representing a gravitational well. 
  The project is built using <b>pygame</b> and <b>ModernGL</b>, with dependency management handled by the 
  blazing-fast <a href="https://github.com/astral-sh/uv">uv package manager</a>.
</p>

<hr/>

<h2>🚀 Features</h2>
<ul>
  <li><b>pygame</b> – for window creation, input handling, and game loop management.</li>
  <li><b>ModernGL</b> – for modern OpenGL rendering and high-performance graphics.</li>
  <li><b>uv</b> – for fast, reproducible dependency management.</li>
</ul>

<hr/>

<h2>🛠 Work in Progress / Upcoming Features</h2>
<ul>
  <li>Adding planets to the simulation</li>
  <li>Visualizing the effect of the sun’s gravity on planets</li>
  <li>Improved gravitational well rendering</li>
</ul>

<hr/>

<h2>📦 Installation</h2>

<h3>Prerequisites</h3>
<ul>
  <li>Python 3.9+ (recommended)</li>
  <li><a href="https://github.com/astral-sh/uv">uv</a> installed globally:</li>
</ul>

<pre><code>curl -LsSf https://astral.sh/uv/install.sh | sh
</code></pre>

<h3>Clone the repository</h3>
<pre><code>git clone https://github.com/your-username/your-project.git
cd your-project
</code></pre>

<h3>Install dependencies with uv</h3>
<pre><code>uv venv
source .venv/bin/activate   # On macOS/Linux
.venv\Scripts\activate      # On Windows

uv pip install -r requirements.txt
</code></pre>

<hr/>

<h2>🛠 Dependencies</h2>
<p>The project depends on:</p>
<ul>
  <li>pygame</li>
  <li>moderngl</li>
</ul>

<p>If you add more dependencies, just update <code>requirements.txt</code>:</p>
<pre><code>uv pip freeze > requirements.txt
</code></pre>

<hr/>

<h2>▶️ Running the Project</h2>
<pre><code>python main.py
</code></pre>

<hr/>

<h2>🧩 Project Structure</h2>
<pre><code>your-project/
│── main.py          # Entry point
│── requirements.txt # Project dependencies
│── README.md        # Project documentation
│── assets/          # Game assets (images, sounds, shaders, etc.)
│── src/             # Source code modules
</code></pre>

<hr/>

<h2>🤝 Contributing</h2>
<ol>
  <li>Fork the repo</li>
  <li>Create a feature branch (<code>git checkout -b feature-name</code>)</li>
  <li>Commit changes (<code>git commit -m "Add new feature"</code>)</li>
  <li>Push to branch (<code>git push origin feature-name</code>)</li>
  <li>Open a Pull Request</li>
</ol>

<hr/>

<h2>📄 License</h2>
<p>This project is licensed under the <a href="LICENSE">MIT License</a>.</p>
