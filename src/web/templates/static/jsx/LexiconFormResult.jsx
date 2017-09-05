window.LexiconFormResult = React.createClass({

    componentDidMount: function() {
        var table = $('#lexicon-results').DataTable({
            data: [],
            columns: [{ title: "Surface form" }, { title: "Tag" }, { title: "Lemma" }]
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

        if (this.props.error != null) {
            return <div className="error-message">{this.props.error}</div>;
        }

        var style = {
            display: this.props.result == undefined ? 'none' : 'block'
        }

        return (
            <div className="form-group" style={style}>
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
                            <textarea readOnly="true" className="form-control"
                                        rows="20" value={this.props.result ? JSON.stringify(this.props.result.data) : ''}>

                            </textarea>
                        </div>
                    </ReactBootstrap.Tab>
                </ReactBootstrap.Tabs>
            </div>
        )
    }
});

