export type Flight = {
  depart: string;
  "depart code": string;
  arrival: string;
  "arrival code": string;
  date: string;
  "flight number": string;
  "airline code": string;
  "Special Service Requests": string[];
  "remarks about the fly": string[];
};

export type PassengerData = {
  "passengers name": string[];
  flights: Flight[];
  "ticket numnber": string[];
  "general remarks": string[];
};

export type UpdateType = {
  "modification date": string;
  object: string;
  author: string;
  agency: string;
};

export type AnswerType = {
  summary: PassengerData;
  updates: UpdateType[];
  pnr_number: string;
};

export type FlightInfo = {
  depart: string;
  arrival: string;
  changes_conditions: {
    before_departure: string;
    no_show_at_first_flight: string;
    after_departure: string;
    no_show_at_subsequent_flight: string;
  };
  refund_conditions: {
    before_departure: string;
    no_show_at_first_flight: string;
    after_departure: string;
    no_show_at_subsequent_flight: string;
  };
};
