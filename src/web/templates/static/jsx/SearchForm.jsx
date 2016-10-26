window.SearchForm = React.createClass({

    taggerRequest: function() {

        var file = $('#tagger-file-chooser').val();
        var text = this.state.taggerForm.inputText;
        var inputFormat = this.state.taggerForm.format;
        var method = this.state.taggerForm.method;
        var language = this.state.taggerForm.language;

        if ((!file && !text) || !inputFormat || !method) {
            return;
        }

        var url = baseUrl + language + '/' + method;
        var data = new FormData();
        data.append('format', inputFormat);

        var requestId = generateGuid();

        data.append('request-id', requestId);
        if (file) {
            data.append('file', $('#tagger-file-chooser')[0].files[0]);
        } else {
            data.append('text', text)
        }

        var newState = React.addons.update(this.state, {
            taggerForm: {
                isInProcessing: { $set: true },
                requestId: { $set: requestId }
            }
        });
        this.setState(newState);

        var sendDate = (new Date()).getTime();
        var trHTML = '';
        $('#results').empty();

        var self = this;
        jQuery.ajax({
            type: "POST",
            dataType: inputFormat == 'json' ? 'json' : 'xml',
            url: url,
            data: data,
            processData: false,
            contentType: false,
            success: function(data, status, xml) {
                var newState = React.addons.update(self.state, {
                    taggerForm: {
                        result: { $set: { data: data, raw: xml }},
                        lastQueryFormat: { $set: inputFormat }
                    }
                });
                self.setState(newState);
            }, error: function(response) {

            },
            complete: function(data) {
                var newState = React.addons.update(self.state, {
                    taggerForm: {
                        isInProcessing: { $set: false }
                    }
                });
                self.setState(newState);
            }
        });
    },

    getInitialState: function() {
        return {
            taggerForm: {
                inputText: "",
                format: "json",
                method: "tag",
                language: "hr",
                isFileSelected: false,
                result: {},
                requestId: "",
                lastQueryFormat: "json"
            },
            lexiconForm: {

            }
        }
    },

    clearTaggerForm: function() {
        this.setState({
            taggerForm: this.getInitialState().taggerForm
        });
    },

    clearLexiconForm: function() {
        this.setState({
            lexiconForm: this.getInitialState().lexiconForm
        });
    },

    changeTaggerFormField: function(field, event) {
        var taggerForm = this.state.taggerForm;
        taggerForm[field] = event.target.value;
        this.setState({
            taggetForm: taggerForm
        });
    },

    onFileSelect: function() {
        var taggerForm = this.state.taggerForm;
        taggerForm.isFileSelected = true;
        this.setState({
            taggetForm: taggerForm
        });
    },

    onFileDeselect: function() {
        var taggerForm = this.state.taggerForm;
        taggerForm.isFileSelected = false;
        this.setState({
            taggerForm: taggerForm
        });
    },

    render: function() {

        var data = {};
        if(this.state.taggerForm.lastQueryFormat == "json") {
            data.json = this.state.taggerForm.result.data;
            data.raw  = JSON.stringify(this.state.taggerForm.result.data, null, 4);
        } else {
            data.json  = JSON.parse(xml2json(this.state.taggerForm.result.data, ''))["D-Spin"]["TextCorpus"];
            data.raw   = this.state.taggerForm.result.raw.responseText;
        }

        return (
            <ReactBootstrap.Tabs defaultActiveKey={1} id="uncontrolled-tab-example" bsStyle="pills">
                <ReactBootstrap.Tab eventKey={1} title="Tagger">
                    <div className="col-md-12">
                        <TaggerForm
                            model={this.state.taggerForm}
                            changeField={this.changeTaggerFormField}
                            onFileSelect={this.onFileSelect}
                            onFileDeselect={this.onFileDeselect}
                            clearForm={this.clearTaggerForm}
                            onSubmit={this.taggerRequest}
                        />
                    </div>
                    <div className="col-md-12">
                        <TaggerFormResult
                            result={data}
                            requestId={this.state.taggerForm.requestId}
                            downloadUrl={this.props.downloadUrl}
                            format={this.state.taggerForm.lastQueryFormat}
                        />
                    </div>
                </ReactBootstrap.Tab>
                <ReactBootstrap.Tab eventKey={2} title="Lexicon">
                    <div className="col-md-5">
                        <LexiconForm model={this.state.lexiconForm} />
                    </div>
                    <div className="col-md-7">
                        <LexiconFormResult />
                    </div>
                </ReactBootstrap.Tab>
            </ReactBootstrap.Tabs>
        )

    }
});