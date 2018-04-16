window.TaggerForm = React.createClass({

    removeFile: function(e) {
        e.preventDefault();
        $('#tagger-file-chooser').val('');
        this.props.onFileDeselect();
    },

    clearForm: function(e) {
        e.preventDefault();
        $('#tagger-file-chooser').val('');
        this.props.clearForm();
    },

    submit: function(e) {
        e.preventDefault();
        this.props.onSubmit();
    },

    render: function() {

        var submitButtonText = this.props.model.isInProcessing ? 'Processing ...' : 'Process';

        return (
            <form id="search-form" className="form-horizontal tab-pane fade in">
                <fieldset>
                    <div className="col-md-6">
                        <div className="bordered">
                            <div className="form-group">
                                <label htmlFor="input-text" className="col-md-12 control-label" style={{textAlign: 'left'}}>Text</label>
                                <div className="col-md-12">
                                    <textarea className="form-control" rows="10" id="input-text"
                                        disabled={this.props.model.isFileSelected}
                                        style={{border: '1px solid #E8E7E7'}}
                                        value={this.props.model.inputText}
                                        onChange={this.props.changeField.bind(null, 'inputText')}>
                                    </textarea>
                                </div>
                            </div>
                            <div className="separator"><span>or</span></div>
                            <div className="form-group">
                                <label htmlFor="input-text" className="col-md-2 control-label no-top-padding">File</label>
                                <div className="col-md-7">
                                    <input id="tagger-file-chooser" type="file" name="input-file"
                                        onChange={this.props.onFileSelect} />
                                </div>
                                <button id="remove-file" className="btn btn-primary btn-xs no-top-margin" onClick={this.removeFile}>
                                    remove
                                </button>
                            </div>
                        </div>
                    </div>
                    <div className="col-md-6">
                        <LanguagePicker options={this.props.languageOptions} selected={this.props.model.language}
                            onChange={this.props.changeField.bind(null, 'language')}/>

                        <div className="form-group">
                            <label className="col-md-2 control-label">Format</label>
                            <div className="col-md-10">
                                <label className="radio-inline">
                                    <input type="radio" name="input-format" id="input-format-1" value="json"
                                            checked={this.props.model.format == 'json'}
                                            onChange={this.props.changeField.bind(null, 'format')} />
                                    Text
                                </label>
                                <label className="radio-inline">
                                    <input type="radio" name="input-format" id="input-format-2" value="tcf"
                                            checked={this.props.model.format == 'tcf'}
                                            onChange={this.props.changeField.bind(null, 'format')}/>
                                    TCF
                                </label>
                            </div>
                        </div>

                        <div className="form-group">
                            <label className="col-md-2 control-label">Function</label>
                            <div className="col-md-10">
                                <label className="radio-inline">
                                    <input type="radio" name="method" id="method1" value="tag"
                                            checked={this.props.model.method == 'tag'}
                                            onChange={this.props.changeField.bind(null, 'method')} />
                                    Tag
                                </label>
                                <label className="radio-inline">
                                    <input type="radio" name="method" id="method2" value="lemmatise"
                                            checked={this.props.model.method == 'lemmatise'}
                                            onChange={this.props.changeField.bind(null, 'method')} />
                                    Lemmatise
                                </label>
                                <label className="radio-inline">
                                    <input type="radio" name="method" id="method3" value="tag_lemmatise"
                                            checked={this.props.model.method == 'tag_lemmatise'}
                                            onChange={this.props.changeField.bind(null, 'method')} />
                                    Tag  +  Lemmatise
                                </label>
                            </div>
                            <div className="col-md-10 col-md-offset-2">
                                <label className="radio-inline">
                                    <input type="radio" name="method" id="method4" value="tag_lemmatise_ner"
                                            checked={this.props.model.method == 'tag_lemmatise_ner'}
                                            onChange={this.props.changeField.bind(null, 'method')} />
                                    Tag + Lemmatise + NER
                                </label>
                            </div>
                            <div className="col-md-10 col-md-offset-2">
                                <label className="radio-inline">
                                    <input type="radio" name="method" id="method5" value="tag_lemmatise_depparse"
                                            checked={this.props.model.method == 'tag_lemmatise_depparse'}
                                            onChange={this.props.changeField.bind(null, 'method')} />
                                    Tag  +  Lemmatise  +  Dep Parse
                                </label>
                            </div>
                        </div>
                        <div className="form-group">
                            <div className="col-md-10 col-md-offset-2">
                                <button id="search-button" type="submit" className="btn btn-primary" onClick={this.submit}>
                                    {submitButtonText}
                                </button>
                                <button id="tagger-clear-button" type="submit" className="btn btn-primary clear-tag" onClick={this.clearForm}>Clear</button>
                            </div>
                        </div>
                    </div>
                </fieldset>
            </form>
        )
    }
});