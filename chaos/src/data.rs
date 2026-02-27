use axum::{http::StatusCode, response::IntoResponse, Json};
use serde::{Deserialize, Serialize};

pub async fn process_data(Json(request): Json<DataRequest>) -> impl IntoResponse {
    // Calculate sums and return response

    let mut string_len = 0;
    let mut int_sum = 0;

    for item in request.data {
        match item {
            DataItem::Str(str) => string_len += str.len() as i64,
            DataItem::Int(number) => int_sum += number,
        }
    }

    let response = DataResponse {
        string_len,
        int_sum
    };

    (StatusCode::OK, Json(response))
}

#[derive(Deserialize)]
pub struct DataRequest {
    pub data: Vec<DataItem>
}

#[derive(Serialize)]
pub struct DataResponse {
    pub string_len: i64,
    pub int_sum: i64,
}

#[derive(Deserialize)]
#[serde(untagged)]
pub enum DataItem {
    Str(String),
    Int(i64),
}