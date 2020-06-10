
<h1>Search article with engine SOLR</h1>

<strong>Set up environment</strong>
<ul>
    <li>Create new env in python</li>
    <code>conda create -n solr</code>
    <li>Activate env</li>
    <code>conda activate solr</code>
    <li>Install requirement package</li>
    <code>pip install -r requirements.txt</code>
</ul>
<strong>Make sure</strong>
<ul>
    <li>Run solr server with port: 8983</li>
    <li>Create core with name is: bkcv</li>
    <p style="background-color: lightgray; font-style: italic; width: 300px;">Note: You can change inside config file</p>
</ul>
<strong>Run and features</strong>
<ul>
    <li>To run server:</li>
    <code>python solr_server.py</code>
    <li>To add data</li>
    <ul>
        <li>get localhost:5000/add_data</li>
    </ul>
    <li>To delete data</li>
    <ul>
        <li>get localhost:5000/api/delete_data</li>
    </ul>
</ul>
