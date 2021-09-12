import React from 'react';
import { Carousel, Row, Col } from 'antd';
import apiaryList from '../images/intro/apiaries.png';
import hiveList from '../images/intro/hives.png';
import hiveDetails from '../images/intro/hives_detail.png';
import hiveEvents from '../images/intro/hives_events.png';


const TRADS = {
  "en": {
    WELCOME: "Welcome to AKingBee !",
    INTRODUCTION: <p>A place dedicated to bees, for beekeepers !<br/>This online tool helps you to manage all your activity, from the apiries down to the swarms</p>,
    APIARIES_DESC: "Register all your apiaries !",
    HIVES_DESC: "Easily manage your hives from a single place !",
    HIVES_DETAILS: "Have a in-depth follow-up for each one of your hives !",
    HIVES_EVENTS: "Planify future events and follow-up on them later on !",
    BOTTOM_WORDS: <p>Please keep in mind this website is maintained by a single person. Any feedback to contact@akingbee.com would be more than welcome ! Also do keep in mind that the tool is completely free and your data is safe. Credentials data is encrypted and your data will not be sold/provided to any third party.</p>,
  },
  "fr": {
    WELCOME: "Bienvenue sur AKingBee !",
    INTRODUCTION: <p>Un endroit dédié aux abeilles, pour les apiculteurs !<br/>Cet outil en ligne vous permet de gérer votre activité d'apiculteur, des ruches jusqu'aux essaims</p>,
    APIARIES_DESC: "Déclarer vos ruchers !",
    HIVES_DESC: "Gérer facilement toutes vos ruches d'un seul point central !",
    HIVES_DETAILS: "Ayez un suivi en profondeur pour chacune de vos ruches !",
    HIVES_EVENTS: "Planifier vos actions futures et faites un suivi plus tard !",
    BOTTOM_WORDS: <p>Gardez à l'esprit que ce site est maintenu par une seule personne. Tout retour est le bienvenue sur contact@akingbee.com ! Cet outil est complètement gratuit, vos informations de connections sont encriptées et vos données ne seront jamais vendues/fournies à un quelconque tiers.</p>,
  }

}

export function WelcomePage(props) {
  let contentStyle = {
    lineHeight: '20px',
    textAlign: 'center',
    background: '#ffffff',
    paddingTop: "40px"
  };

  return (
    <>
      <Row>
        <Col offset={2} span={20}>
          <h2 style={{textAlign:"center", padding:"20px"}}>{TRADS[window.currentLanguage].WELCOME}</h2>
          {TRADS[window.currentLanguage].INTRODUCTION}
        </Col>
      </Row>
      <Row style={{marginTop: "15px"}} justify="center">
        <Col span={20}>
          <Carousel dotPosition="top" autoplaySpeed={7000} autoplay>
            <div>
              <h3 style={contentStyle}>
                <Row justify="center">
                  {TRADS[window.currentLanguage].APIARIES_DESC}
                </Row>
                <Row>
                  <div style={{border: "2px solid #aaaaaa", borderRadius: "5px", margin: "20px"}}>
                    <img src={apiaryList} width="100%"/>
                  </div>
                </Row>
                <Row>
                </Row>
              </h3>
            </div>
            <div>
              <h3 style={contentStyle}>
                <Row justify="center">
                  {TRADS[window.currentLanguage].HIVES_DESC}
                </Row>
                <Row>
                  <div style={{border: "2px solid #aaaaaa", borderRadius: "5px", margin: "20px"}}>
                    <img src={hiveList} width="100%"/>
                  </div>
                </Row>
                <Row>
                </Row>
              </h3>
            </div>
            <div>
              <h3 style={contentStyle}>
                <Row justify="center">
                  {TRADS[window.currentLanguage].HIVES_DETAILS}
                </Row>
                <Row>
                  <div style={{border: "2px solid #aaaaaa", borderRadius: "5px", margin: "20px"}}>
                    <img src={hiveDetails} width="100%"/>
                  </div>
                </Row>
                <Row>
                </Row>
              </h3>
            </div>
            <div>
              <h3 style={contentStyle}>
                <Row justify="center">
                  {TRADS[window.currentLanguage].HIVES_EVENTS}
                </Row>
                <Row>
                  <div style={{border: "2px solid #aaaaaa", borderRadius: "5px", margin: "20px"}}>
                    <img src={hiveEvents} width="100%"/>
                  </div>
                </Row>
                <Row>
                </Row>
              </h3>
            </div>
          </Carousel>
        </Col>
      </Row>
      <Row>
        <Col offset={2} span={20}>
          {TRADS[window.currentLanguage].BOTTOM_WORDS}

        </Col>
      </Row>
    </>
  )
}