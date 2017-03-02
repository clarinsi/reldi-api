window.TaggerFormResult = React.createClass({

    render: function() {

        if (this.props.error != null) {
            return <div className="error-message">{this.props.error}</div>;
        }

        var result = this.props.result;
        if (!result.json) {
            return false;
        }

        // Normalize data
        if (!Array.isArray(result.json.tokens.token)) {
            result.json.tokens.token = [result.json.tokens.token];
        }
        if ('POStags' in result.json && !Array.isArray(result.json.POStags.tag)) {
            result.json.POStags.tag = [result.json.POStags.tag];
        }
        if ('lemmas' in result.json && !Array.isArray(result.json.lemmas.lemma)) {
            result.json.lemmas.lemma = [result.json.lemmas.lemma];
        }
        if ('depparsing' in result.json && !Array.isArray(result.json.depparsing.parse)) {
            result.json.depparsing.parse = [result.json.depparsing.parse];
        }
        if ('depparsing' in result.json && !Array.isArray(result.json.depparsing.parse[0].dependency)) {
            result.json.depparsing.parse[0].dependency = [result.json.depparsing.parse[0].dependency];
        }

        // Generate table
        var tableHeaders = [<th key="idx"></th>, <th key="surface">Surface</th>];
        if ('POStags' in result.json) {
            tableHeaders.push(<th key="tags">Tags</th>);
        }
        if ('lemmas' in result.json) {
            tableHeaders.push(<th key="lemma">Lemma</th>);
        }
        if ('depparsing' in result.json) {
            tableHeaders.push(<th key="depparse">Dep parse - gov / func</th>);
        }

        tableHeaders.push(<th key="echr">Start char</th>);
        tableHeaders.push(<th key="schr">End char</th>);

        var sentenceIdx = 0;
        var previousSentenceSum = 0;
        var tokens = result.json.tokens.token;

        var bodyRows = result.json.tokens.token.map(function(row, idx) {
            var tds = [];
            tds.push(<td key="idx"><strong>{idx - previousSentenceSum + 1}.</strong></td>);
            tds.push(<td key="surf">{row.text}</td>);

            if ('POStags' in result.json) {
                tds.push(<td key="tags">{result.json.POStags.tag[idx].text}</td>)
            }

            if ('lemmas' in result.json) {
                tds.push(<td key="lemma">{result.json.lemmas.lemma[idx].text}</td>)
            }

            if ('depparsing' in result.json) {
                var govIds = result.json.depparsing.parse[sentenceIdx].dependency[idx - previousSentenceSum].govIDs;
                if (govIds == undefined) {
                    govIds = '0'
                } else {
                    govIds = (parseInt(govIds.split("t_")[1]) + 1) - previousSentenceSum;
                }

                var func = result.json.depparsing.parse[sentenceIdx].dependency[idx - previousSentenceSum].func;
                tds.push(<td key="depparse">{govIds} / {func}</td>)
            }

            tds.push(<td key="schr">{row.startChar}</td>);
            tds.push(<td key="echr">{row.endChar}</td>);


            if ('depparsing' in result.json && (idx - previousSentenceSum == result.json.depparsing.parse[sentenceIdx].dependency.length - 1)) {
                previousSentenceSum += (result.json.depparsing.parse[sentenceIdx].dependency.length);
                sentenceIdx++;
            }

            var style = {};
            if (idx - previousSentenceSum == 0) {
                style.borderTop = '50px solid white';
            }


            return (<tr style={style} key={idx}>{tds}</tr>);
        });

        return (
            <div className="form-group">
                <label htmlFor="textArea" className="col-md-12 control-label">Result</label>
                <ReactBootstrap.Tabs defaultActiveKey={1} id="uncontrolled-tab-example" bsStyle="pills">
                    <ReactBootstrap.Tab eventKey={1} title="Table">
                        <table id="lexicon-results" className="table" cellSpacing="0" width="100%" >
                            <thead>
                                <tr>
                                    {tableHeaders}
                                </tr>
                            </thead>
                            <tbody>
                                {bodyRows}
                            </tbody>
                        </table>
                    </ReactBootstrap.Tab>
                    <ReactBootstrap.Tab eventKey={2} title="Raw">
                        <div className="col-md-12">
                            <textarea readOnly="true" className="form-control" rows="20" value={result.raw} />
                        </div>
                    </ReactBootstrap.Tab>
                    <ReactBootstrap.Tab eventKey={3} title="Download">
                        <div className="col-md-12">
                            <a href={this.props.downloadUrl + this.props.requestId}
                                disabled={this.props.requestId == ''}>Download</a>
                        </div>
                    </ReactBootstrap.Tab>
                </ReactBootstrap.Tabs>
            </div>
        )
    }
});

