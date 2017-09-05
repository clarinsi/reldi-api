window.LanguagePicker = React.createClass({

    options: React.PropTypes.array.isRequired,
    selected: React.PropTypes.string.isRequired,

    render: function() {

        var self = this;
        var options = this.props.options.map(function(option) {
            return <option key={option.value} value={option.value}>{option.label}</option>
        });

        return (
            <div className="form-group">
                <label className="col-md-2 control-label">Language</label>
                <div className="col-md-4">
                    <select defaultValue={self.props.selected} onChange={this.props.onChange}>
                        {options}
                    </select>
                </div>
            </div>
        )
    }
});