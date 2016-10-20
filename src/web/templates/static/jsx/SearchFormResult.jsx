window.SearchFormResult = React.createClass({
    render: function() {
        return (
            <div className="form-group">
                <label htmlFor="textArea" className="col-md-12 control-label">Result</label>
                <ReactBootstrap.Tabs defaultActiveKey={2} id="uncontrolled-tab-example" bsStyle="pills">
                    <ReactBootstrap.Tab eventKey={1} title="Table">
                        <table id="lexicon-results" className="table" cellSpacing="0" width="100%" >
                            <thead>
                                <tr>
                                    <th>Surface</th>
                                    <th>Tags</th>
                                    <th>Lemma</th>
                                </tr>
                            </thead>
                        </table>
                    </ReactBootstrap.Tab>
                    <ReactBootstrap.Tab eventKey={2} title="Raw">
                        <div className="col-md-12">
                            <textarea id="result-area" readOnly="true" className="form-control" rows="20"></textarea>
                            <textarea id="lexicon-result-area" readOnly="true" className="form-control" rows="20"></textarea>
                        </div>
                    </ReactBootstrap.Tab>
                    <ReactBootstrap.Tab eventKey={3} title="Download">
                        <a id="download-result" href="{{ url_for('web_router.download', requestId='') }}"
                                target="_blank" className="btn btn-default"
                                style={{margin: 0, textTransform: 'none'}}>
                            Download
                        </a>
                    </ReactBootstrap.Tab>
                </ReactBootstrap.Tabs>
            </div>
        )
    }
});

