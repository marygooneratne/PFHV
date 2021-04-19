mport React from "react";
import {
  Box,
  Card,
  Typography,
  Button,
  requirePropFactory,
  FormLabel,
  FormControl,
  FormGroup,
  FormControlLabel,
  Checkbox,
  ThemeProvider,
} from "@material-ui/core";
import "./../../global.css";
import "./Home.css";
import homeImg from "./../../resources/images/home.jpeg";
import { primaryTheme } from "./../../utils/constants";
import {
  ArgumentAxis,
  ValueAxis,
  Chart,
  LineSeries,
} from "@devexpress/dx-react-chart-material-ui";
const mockProps = {
  homeData: {
    address: "25681 Estoril Street, Valencia CA 91355",
    bedrooms: 4,
    bathrooms: 2,
    squareFeet: 3000,
    imgSrc: homeImg,
  },
  values: ["$700,000", "$820,000", "$1,300,000"],
};
const modelParams = [
  "Square Feet",
  "Zipcode",
  "Bedrooms",
  "Bathrooms",
  "Housing Marking Index",
];

const data = [
  { value: 720000, year: 1 },
  { value: 800000, year: 5 },
  { value: 1300000, year: 10 },
];
function Home(props) {
  props = mockProps;
  return (
    <ThemeProvider theme={primaryTheme}>
      <Box className="home-box rows">
        <Button className="return-button" variant="contained" color="primary">
          Return to list
        </Button>
        <Box className="home-cards cols">
          <Card variant="outlined" className="home-info-card card">
            <img className="home-image" src={homeImg} />
            <Box className="home-info-text">
              <Typography className="home-address" variant="h6">
                {props.homeData.address}
              </Typography>
              <Typography variant="body">
                Bedrooms: {props.homeData.bedrooms}
                <br />
                Bathrooms: {props.homeData.bathrooms}
                <br />
                Sqft.: {props.homeData.squareFeet}
              </Typography>
            </Box>
          </Card>
          <Card variant="outlined" className="home-info-card card">
            <img className="home-image" src={homeImg} />
            <Box className="home-info-text">
              <Typography className="home-address" variant="h6">
                {props.homeData.address}
              </Typography>
              <Typography variant="body">
                Bedrooms: {props.homeData.bedrooms}
                <br />
                Bathrooms: {props.homeData.bathrooms}
                <br />
                Sqft.: {props.homeData.squareFeet}
              </Typography>
            </Box>
          </Card>
          <Card variant="outlined" className="home-info-card card">
            <img className="home-image" src={homeImg} />
            <Box className="home-info-text">
              <Typography className="home-address" variant="h6">
                {props.homeData.address}
              </Typography>
              <Typography variant="body">
                Bedrooms: {props.homeData.bedrooms}
                <br />
                Bathrooms: {props.homeData.bathrooms}
                <br />
                Sqft.: {props.homeData.squareFeet}
              </Typography>
            </Box>
          </Card>
          <Card variant="outlined" className="growth-card card">
            <Typography className="growth-card-title" variant="h6">
              Projected Value
            </Typography>
            <Chart data={data} className="model-chart">
              <ArgumentAxis />
              <ValueAxis />

              <LineSeries valueField="value" argumentField="year" />
            </Chart>
            <Typography variant="body">
              1Y: {props.values[0]}
              <br />
              5Y: {props.values[1]}
              <br />
              10Y: {props.values[2]}
            </Typography>
          </Card>
        </Box>
      </Box>
    </ThemeProvider>
  );
}
export default Home;