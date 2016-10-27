window.LexiconFormResult = React.createClass({

    componentDidMount: function() {
        var table = $('#lexicon-results').DataTable({
            data: [],
            columns: [{ title: "Surface from" }, { title: "Tags" }, { title: "Lemma" }]
        });
    },

    componentWillReceiveProps: function(nextProps) {
        if (nextProps.result == undefined) {
            return;
        }

        if (this.props.result && nextProps.result.hash == this.props.result.hash) {
            return;
        }

        var table = $('#lexicon-results').dataTable();
        table.fnClearTable();
        if (nextProps.result.data.length > 0) {
            table.fnAddData(nextProps.result.data);
        }
    },

    render: function() {
        return (
            <div className="form-group">
                <label htmlFor="textArea" className="col-md-12 control-label">Result</label>
                <ReactBootstrap.Tabs defaultActiveKey={1} id="uncontrolled-tab-example" bsStyle="pills">
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
                </ReactBootstrap.Tabs>
            </div>
        )
    }
});

