window.SearchForm = React.createClass({

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
                payload: {
                    surface: "",
                    surface_is_regex: false,
                    lemma: "",
                    lemma_is_regex: false,
                    msd: "",
                    msd_is_regex: false,
                    no_of_syllables: "",
                    language: "hr",
                }
            }
        }
    },

    calculateDatasetHash: function(dataset) {
        var hash = 0;
        dataset.forEach(function(row) {
            var concat = '';
            row.forEach(function(item) {
                concat = concat + item;
            });
            hash = hex_md5(hash + '-' + concat);
        });
        return hash;
    },

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
                        lastQueryFormat: { $set: inputFormat },
                        error: { $set: null }
                    }
                });
                self.setState(newState);
            }, error: function(response) {
                var newState = React.addons.update(self.state, {
                    taggerForm: {
                        error: { $set: response.responseText }
                    }
                });
                self.setState(newState);
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

    lexiconRequest: function() {
        var payload= JSON.parse(JSON.stringify(this.state.lexiconForm.payload));
        var language = payload.language;
        delete payload.language;

        if (payload.lemma == "" && payload.surface == "" && payload.msd == "") {
            return;
        }

        payload.surface_is_regex = payload.surface_is_regex ? '1' : '0';
        payload.lemma_is_regex   = payload.lemma_is_regex   ? '1' : '0';
        payload.msd_is_regex     = payload.msd_is_regex     ? '1' : '0';

        var method = 'lexicon';
        var url = baseUrl + language + '/' + method;
        var sendDate = (new Date()).getTime();

        var newState = React.addons.update(this.state, {
            lexiconForm: {
                isInProcessing: { $set: true }
            }
        });
        this.setState(newState);

        var self = this;
        jQuery.ajax({
            type: "GET",
            dataType: 'json',
            url: url,
            data: payload
        }).success(function(data) {

            var hash = self.calculateDatasetHash(data.result);
            var dataset = {
                data: data.result,
                hash: hash
            }
            var newState = React.addons.update(self.state, {
                lexiconForm: {
                    result: { $set: dataset },
                    error:  { $set: null }
                }
            });
            self.setState(newState);
        }).fail(function(response) {
            var newState = React.addons.update(self.state, {
                lexiconForm: {
                    error: { $set: response.responseText }
                }
            });
            self.setState(newState);
        }).always(function() {
            var receiveDate = (new Date()).getTime();
            var responseTimeMs = receiveDate - sendDate;
            var newState = React.addons.update(self.state, {
                lexiconForm: {
                    isInProcessing: { $set: false },
                    responseTime: { $set: responseTimeMs }
                }
            });
            self.setState(newState);
        });
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

    changeLexiconFormField: function(field, isCheckbox, event) {

        var lexiconForm = this.state.lexiconForm;
        if (isCheckbox) {
            lexiconForm.payload[field] = event.target.checked;
        } else {
            lexiconForm.payload[field] = event.target.value;
        }
        this.setState({
            lexiconForm: lexiconForm
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

        var languageOptions = [
            {
               value: "hr",
               label: "Croatian"
            },
            {
               value: "sr",
               label: "Serbian"
            },
            {
               value: "sl",
               label: "Slovenian"
            },
        ];

        var data = {};
        if(this.state.taggerForm.lastQueryFormat == "json") {
            data.json = this.state.taggerForm.result.data;
            data.raw  = JSON.stringify(this.state.taggerForm.result.data, null, 4);
        } else {
            data.json = JSON.parse(xml2json(this.state.taggerForm.result.data, ''))["D-Spin"]["TextCorpus"];
            data.raw  = this.state.taggerForm.result.raw.responseText;
        }

        return (
            <ReactBootstrap.Tabs defaultActiveKey={1} id="uncontrolled-tab-example" bsStyle="pills">
                <ReactBootstrap.Tab eventKey={1} title="Tagger">
                    <div className="col-md-12">
                        <TaggerForm
                            model={this.state.taggerForm}
                            languageOptions={languageOptions}
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
                            error={this.state.taggerForm.error}
                            requestId={this.state.taggerForm.requestId}
                            downloadUrl={this.props.downloadUrl}
                            format={this.state.taggerForm.lastQueryFormat}
                        />
                    </div>
                </ReactBootstrap.Tab>
                <ReactBootstrap.Tab eventKey={2} title="Lexicon">
                    <div className="col-md-5">
                        <LexiconForm
                            model={this.state.lexiconForm.payload}
                            error={this.state.lexiconForm.error}
                            isInProcessing={this.state.lexiconForm.isInProcessing}
                            languageOptions={languageOptions}
                            changeField={this.changeLexiconFormField}
                            clearForm={this.clearLexiconForm}
                            onSubmit={this.lexiconRequest}
                         />
                    </div>
                    <div className="col-md-7">
                        <LexiconFormResult result={this.state.lexiconForm.result} error={this.state.lexiconForm.error} />
                    </div>
                </ReactBootstrap.Tab>
            </ReactBootstrap.Tabs>
        )

    }
});