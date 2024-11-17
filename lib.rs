use solana_program::{
    account_info::AccountInfo,
    entrypoint,
    entrypoint::ProgramResult,
    pubkey::Pubkey,
    msg,
};

/// Define the program's entrypoint
entrypoint!(process_instruction);

/// Main function where program logic is handled
fn process_instruction(
    program_id: &Pubkey,           // The program ID of this program
    accounts: &[AccountInfo],     // List of accounts passed to the program
    instruction_data: &[u8],      // Instruction data passed to the program
) -> ProgramResult {
    // Example: Print a debug message
    msg!("Hello, Solana!");

    // Add logic here (e.g., data manipulation or validation)
    if instruction_data.is_empty() {
        msg!("No instruction data provided.");
    } else {
        msg!("Instruction data: {:?}", instruction_data);
    }

    Ok(())
}