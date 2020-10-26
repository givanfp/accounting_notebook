import React, { Component } from "react";
import { render } from "react-dom";
import Button from 'react-bootstrap/Button';
import Accordion from 'react-bootstrap/Accordion';
import Card from 'react-bootstrap/Card';

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      data: [],
      loaded: false,
      placeholder: "Loading"
    };
  }
  componentDidMount() {
    fetch("/api/transactions/")
      .then(response => {
        if (response.status > 400) {
            console.log(response)
          return this.setState(() => {
            return { placeholder: "Something went wrong!" };
          });
        }
        return response.json();
      })
      .then(data => {
        this.setState(() => {
          return {
            data,
            loaded: true
          };
        });
      });
  }

  render() {
    return (
      <div>
        {this.state.data.map(transaction => {
          const isDebit = transaction.type === "debit"
          const bgColor = transaction.type === "debit" ? "alert-danger" : "alert-success"
          return (
            <Accordion>
            <Card className={bgColor}>
                <Card.Header>
                <Accordion.Toggle as={Button} variant="link" eventKey="0">
                    {transaction.amount} ({transaction.type})
                </Accordion.Toggle>
                </Card.Header>
                <Accordion.Collapse eventKey="0">
                <Card.Body>
                        <p><strong>Transaction Id:</strong> { transaction.id }</p>
                      <p><strong>Amount:</strong> { transaction.amount }</p>
                      <p><strong>Type:</strong> { transaction.type }</p>
                      <p><strong>Effective date:</strong> { transaction.effective_date }</p>
                </Card.Body>
                </Accordion.Collapse>
            </Card>
            </Accordion>
          );
        })}
      </div>
    );
  }
}

export default App;

const container = document.getElementById("app");
render(<App />, container);